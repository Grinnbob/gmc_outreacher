from o24.backend import db
from o24.backend import app
import o24.backend.dashboard.models as models

from o24.backend.models.shared import TaskQueue, TaskQueueLock, Funnel, Action
from o24.globals import *
from .models import Priority, ActionLog
import o24.backend.handlers.jobs_map as jobs_map
import o24.backend.handlers.trail_handlers as trail_handlers
import traceback 

from datetime import datetime
import pytz

from mongoengine.queryset.visitor import Q

from o24.exceptions.exception_with_code import ErrorCodeException
from o24.exceptions.error_codes import *
from mongoengine.errors import NotUniqueError
    
class Scheduler():
    def __init__(self):
        pass

    @classmethod
    def lock(cls):
        try:
            locked = TaskQueueLock.objects(lock_key=TASK_QUEUE_LOCK, ack=0).update_one(upsert=True, ack=1)
            if not locked:
                return None

            total = TaskQueueLock.objects(lock_key=TASK_QUEUE_LOCK).count()
            if total > 1:
                raise Exception("...NEVER HAPPENED Scheduler.lock create more than 1 instance")

            scheduler = cls()
            return scheduler
        except Exception as e:
            if type(e) == NotUniqueError:
                return None 

            print(str(e))
            traceback.print_exc()
        
        return None

    def unlock(self):
        return TaskQueueLock.objects(lock_key=TASK_QUEUE_LOCK).update_one(upsert=False, ack=0)


    ###################################### SCHEDULER CYCLE tasks  ##################################
    #################################################################################################
    
    def switch_priority(self):
        # We need to equally select tasks from TaskQueue
        # do_next = intro(0) or follow up(1)
        # follow up level = 0(reserve the current followups) 1(execute followup_level=1 until finished)
        
        current_priority = Priority.get_priority()
        follow_ups = TaskQueue.objects(Q(record_type=FOLLOWUP) & Q(status__ne=FINISHED))
    
        #if we don't have followups then we need to execute INTRO
        if follow_ups.count() <= 0:
            print("follow_ups.count() <= 0")
            current_priority.do_next = INTRO
            current_priority._commit()
            return

        #switch to INTRO if we did followups on the last round
        if current_priority.do_next == FOLLOWUP:
            print("current_priority.do_next == FOLLOWUP")
            current_priority.do_next = INTRO
            current_priority._commit()
            return

        #switch to followup if we did INTRO on the last round
        if current_priority.do_next == INTRO:
            current_priority.do_next = FOLLOWUP
            print("current_priority.do_next == INTRO")

            # we need to check followup_level
            if current_priority.followup_level == 0:
                print("current_priority.followup_level == 0")
                follow_ups.update(followup_level=FOLLOWUP)
                current_priority.followup_level = 1
                current_priority._commit()
                return

            if follow_ups.filter(followup_level=FOLLOWUP).count() <= 0:
                print("follow_ups.filter(followup_level=FOLLOWUP).count() <= 0")
                current_priority.followup_level = 0
                current_priority._commit()
                return
            current_priority._commit()
            return    
    
    def plan(self):
        #All tasks
    
        self.switch_priority()
    
        tasks = TaskQueue.get_ready()
        if tasks:
            print("...scheduler.plan(): found {0} tasks from get_ready".format(tasks.count()))

        for_update = []
    
        for task in tasks:
            try:
                #log task
                ActionLog.log(task, step='plan', description="scheduler.plan()")
                self._switch(task)
                task._commit()
                
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                continue
        
    
    def execute(self):
        current_priority = Priority.get_priority()
        do_next = current_priority.do_next
        followup_level = current_priority.followup_level
        
        print("....scheduler.execute(): current priority do_next={0} followup_level={1}".format(do_next, followup_level))
        tasks = TaskQueue.get_execute_tasks(do_next=do_next, followup_level=followup_level)
        if tasks:
            print("...scheduler.execute(): found {0} tasks from get_execute_tasks".format(tasks.count()))

        jobs = []
        cr_next_actions = {}

        for task in tasks:
            try:
                now = pytz.utc.localize(datetime.utcnow())

                if cr_next_actions.get(task.credentials_id, None) is not None:
                    next_action = cr_next_actions.get(task.credentials_id)
                    if now <= next_action:
                        continue

                credentials = models.Credentials.objects(id=task.credentials_id).first()
                if not credentials:
                    raise Exception("NEVER HAPPENED: can't find credentials_id={0}".format(task.credentials_id))

                has_limits = credentials.change_limits(action_key=task.action_key)
                if not has_limits:
                    continue

                if task.action_key in NON_3RD_PARTY_ACTION_KEYS:
                    handler = jobs_map.JOBS_MAP.get(task.action_key, None)
                    if not handler:
                        raise Exception("There is no handler for key:{0}".format(task.action_key))
                    
                    job = handler.s(str(task.id))
                    jobs.append(job)
        
                task.status = IN_PROGRESS

                task._commit()
                credentials._commit()
                cr_next_actions[credentials.id] = credentials.next_action

                #log task
                ActionLog.log(task, step='execute', description="scheduler.execute(): sent to execution")
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                continue


        self.refresh_campaigns_limits()
    
        return jobs
    
    #Inc counters for each credential (It will change next_action)
    #Refresh next_action for campaigns
    def refresh_campaigns_limits(self):
        campaigns = models.Campaign.objects(status=IN_PROGRESS)
        campaigns_updated = []
        for campaign in campaigns:
            try:
                campaign.change_limits()
                campaigns_updated.append(campaign)
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                continue
        
        models.Campaign.update_campaigns(campaigns_updated)

    def trail(self):
        tasks = TaskQueue.get_trail_tasks()
        if tasks:
            print("...scheduler.trail(): found {0} tasks from get_trail_tasks".format(tasks.count()))

        for task in tasks:
            try:
                if task.status == FAILED:
                    error_code = task.get_code()
                    handler = trail_handlers.FAILED_HANDLERS.get(error_code, None)
                    if handler is None:
                        handler = trail_handlers.FAILED_HANDLERS[TRAIL_UNKNOWN_ERROR]
                    
                    handler(task)
                    continue

                elif task.status == CARRYOUT:
                    action_key = task.action_key
                    handler = trail_handlers.CARRYOUT_HANDLERS.get(action_key, None)
                    if handler is None:
                        handler = trail_handlers.CARRYOUT_HANDLERS[CARRYOUT_DEFAULT_HANDLER]
                    
                    handler(task)
                    continue

                elif task.status in [BLOCK_HAPPENED, NEED_USER_ACTION_RESOLVED]:
                    handler = trail_handlers.BLOCK_HANDLERS.get(tasks.status, None)
                    if handler is None:
                        handler = trail_handlers.BLOCK_HANDLERS[BLOCK_DEFAULT_HANDLER]
                    
                    handler(task)
                    continue
                else:
                    print("Trail unknown status task.id={0} task.status={1} task.action_key={2}".format(task.id, task.status, task.action_key))
                    continue
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                continue
            

    def _switch(self, task):
        if task.status != READY:
            return None
        
        next_node = Funnel.next_node(task.current_node, 
                                    task.result_data)
        if next_node:
            task.switch_task(next_node) 

        return
    ###################################### CAMPAIGN START/PAUSE/RESUME ##################################
    #####################################################################################################
    def start_campaign(self, owner, campaign, input_data=None):
        if campaign.status != NEW:
            return self.resume_campaign(owner=owner, campaign=campaign)

        if campaign._allow_no_prospects():
            self._create_parsing_task(campaign)
            campaign._safe_start()

        else:
            prospects = models.Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
            if not prospects:
                raise Exception("There is no prospects assigned to campaign")

            campaign._safe_start()

            prospect_ids = self._load_prospects(campaign, prospects)
            if not prospect_ids:
                campaign._safe_pause()
                raise Exception("Can't load_prospects campaign_title={0} prospect_ids={1}".format(campaign.title, prospect_ids))

            self._update_prospects(prospect_ids, status=IN_PROGRESS)    
        
        self._setup_scheduler_data(campaign)


    def pause_campaign(self, campaign):
        if not campaign.inprogress():
            return 
            
        # TaskQueue.pause_tasks(campaign_id=campaign.id)

        campaign._safe_pause()
        #campaign.update_status(status=PAUSED)

    def _update_search_task(self, campaign, status):
        task = TaskQueue.objects(campaign_id=campaign.id).first()
        if not task:
            raise Exception("Can't find task for campaign title={0}".format(campaign.title))
        
        task.update_status(status=status)
    

    def _resume_linkedin_parse_campaign(self, owner, campaign):
        if campaign.inprogress():
            raise Exception("Campaign already resumed, title={0}".format(campaign.title))

        self._input_data_refresh(campaign=campaign)

        self._update_search_task(campaign=campaign, status=NEW)

        campaign._safe_start()


    def resume_campaign(self, owner, campaign):
        if campaign.inprogress():
            raise Exception("Campaign already resumed, title={0}".format(campaign.title))
        
        if campaign.campaign_type == LINKEDIN_PARSING_CAMPAIGN_TYPE:
            self._resume_linkedin_parse_campaign(owner=owner, campaign=campaign)
        else:
            self._input_data_refresh(campaign=campaign)

            self._check_new_prospects(owner=owner, campaign=campaign)

            campaign._safe_start()

        #campaign.update_status(status=IN_PROGRESS)

    @classmethod
    def safe_finish_sequence(cls, owner_id, prospects_ids):
        stopped = TaskQueue.objects(prospect_id__in=prospects_ids).update(status=FINISHED)    

        return stopped


    @classmethod
    def safe_unassign_prospects(cls, owner_id, prospects_ids):
        if not owner_id or not prospects_ids:
            return 0

        scheduler = cls()
        #To unassign we need:
        # 1. Pause all campaigns prospects belongs to
        # 2. Remove all tasks from task_queue
        # 3. Update prospects assign_to=None

        campaigns_refs = models.Prospects.objects(owner=owner_id, id__in=prospects_ids).distinct('assign_to')
        if campaigns_refs:
            campaigns_ids = [c.id for c in campaigns_refs]
            campaigns = models.Campaign.objects(owner=owner_id, id__in=campaigns_ids)
            for campaign in campaigns:
                scheduler.pause_campaign(campaign)
        
        tasks_deleted = TaskQueue.safe_unassign_prospects(prospects_ids=prospects_ids)

        prospects_unassigned = models.Prospects._unassign_campaign(owner_id=owner_id, prospects_ids=prospects_ids)    

        return prospects_unassigned

    @classmethod
    def safe_assign_prospects(cls, owner_id, campaign, prospects_ids):
        if not campaign or not prospects_ids:
            return 0

        prospects_without_campaign = models.Prospects.filter_no_campaign(owner_id=owner_id, prospects_ids=prospects_ids)
        if not prospects_without_campaign:
            return 0

        ids = []
        need_data = campaign.need_contacts()

        for p in prospects_without_campaign:
            tags = p.has_all_data(need_data)
            if tags:
                p.add_tags(tags)
                continue
            ids.append(p.id)

        if not ids:
            return 0

        scheduler = cls()
        res = models.Prospects._assign_campaign(owner_id=owner_id, prospects_ids=ids, campaign_id=campaign.id)

        #It's strange - we don't need to create task when we assign campaign
        #res = scheduler.add_prospects(owner=owner_id, campaign=campaign, prospects=prospects_without_campaign)

        if type(res) != list:
            return 0

        return len(res)

    @classmethod
    def safe_start_campaign(cls, owner, campaign):
        if not campaign:
            raise Exception("No such campaign")

        scheduler = cls()
        scheduler.start_campaign(owner=owner, campaign=campaign)

    @classmethod
    def safe_pause_campaign(cls, campaign):
        if not campaign:
            raise Exception("No such campaign")

        scheduler = cls()
        scheduler.pause_campaign(campaign=campaign)


    @classmethod
    def safe_delete_campaign(cls, owner_id, campaign, _unassign=False):
        if not campaign:
            raise Exception("DELETE ERROR: No such campaign")

        if campaign.inprogress():
            raise Exception("DELETE ERROR: campaign in progress, stop it first")

        assigned_prospects = models.Prospects.get_prospects(campaign_id=campaign.id)
        if assigned_prospects:
            if _unassign:
                ids = [p.id for p in assigned_prospects]
                cls.safe_unassign_prospects(owner_id=owner_id, prospects_ids=ids)
            else:
                raise Exception("DELETE ERROR: campaign has prospects, unassign all prospects before delete")

        TaskQueue.delete_campaign(campaign_id=campaign.id)

        return campaign.delete()


    def add_prospects(self, owner, campaign, prospects):
        ids = self._load_prospects(campaign, prospects)
        if not ids:
            raise Exception("Can't load_prospects campaign_title={0} ids={1}".format(campaign.title, ids))
        
        self._update_prospects(ids=ids, status=IN_PROGRESS)

        models.Prospects._assign_campaign(owner_id=owner, prospects_ids=ids, campaign_id=campaign.id)

        return ids


    def _check_new_prospects(self, owner, campaign):
        if not campaign._allow_no_prospects():
            prospects = models.Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
            if prospects:
                self.add_prospects(owner=owner, campaign=campaign, prospects=prospects)

    def _load_prospects(self, campaign, prospects):
        tasks = []

        need_data = campaign.need_contacts()

        for prospect in prospects:
            try:
                tags = prospect.has_all_data(need_data)
                if tags:
                    prospect.add_tags(tags)
                    continue

                task = TaskQueue.create_task(campaign, prospect)
                tasks.append(task)
            except Exception as e:
                print("_load_prospects error: Can't create task for prospect_id={0}".format(prospect.id))
                print(str(e))
                continue

        inserted_tasks = TaskQueue.insert_tasks(tasks)
        prospect_ids = [t.prospect_id for t in inserted_tasks]
        
        return prospect_ids

    def _input_data_refresh(self, campaign):
        tasks = TaskQueue.objects(campaign_id=campaign.id)
        if not tasks:
            return
        
        for task in tasks:
            task.refresh_input_data()
        
        return

    def _create_parsing_task(self, campaign):
        task = TaskQueue.create_task(campaign=campaign, prospect=None)
        task._commit()


    def _update_prospects(self, ids, status):
        models.Prospects.update_prospects(ids, status)

    def _setup_scheduler_data(self, campaign):
        Priority.get_priority()

