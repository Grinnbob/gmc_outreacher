from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Campaign, Prospects
from o24.backend.models.shared import TaskQueue
from o24.globals import *
from .models import Priority, TaskLog

class Scheduler():
    def __init__(self, db, app):
        self.db = db
        self.app = app

    ###################################### SCHEDULER CYCLE tasks  ##################################
    #################################################################################################
    def plan(self):
        #All tasks

        tasks = TaskQueue.get_ready()
        for_update = []
        logs = []

        for task in tasks:
            log = self._switch(task)
            
            for_update.append(task)
            logs.append(log)

        TaskLog.update_logs(logs)
        TaskQueue.update_tasks(for_update)

    def execute(self):
        tasks = TaskQueue.get_execute_tasks()
        for_update = []


    
    def refresh_limits(self):
        pass

    def _switch(self, task):
        if task.status != READY:
            return None
        
        next_node = Funnel.next_node(task.current_node)
        log = TaskLog.create_log(task)
        if next_node:
            task.switch_task(next_node) 

        return log
    ###################################### CAMPAIGN START/PAUSE/RESUME ##################################
    #####################################################################################################
    def start_campaign(self, campaign):
        if campaign.status != NEW:
            raise Exception("You can start only NEW campaign, title={0} status={1}".format(campaign.title, campaign.status))
        
        prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        
        ids = self._load_prospects(campaign, prospects)
        if not ids:
            raise Exception("Can't load_prospects campaign_title={0} ids={1}".format(campaign.title, ids))

        self._update_prospects(ids, status=IN_PROGRESS)    
        
        self._setup_scheduler_data(campaign)

        campaign.update_status(status=IN_PROGRESS)

    def add_prospects(self, campaign, prospects):
        if campaign.status != IN_PROGRESS:
            raise Exception("You can add_prospects only for IN_PROGRESS campaigns, campaign_title={0} campaign_status={1}".format(campaign.title, campaign.status))
        
        ids = self._load_prospects(campaign, prospects)
        if not ids:
            raise Exception("Can't load_prospects campaign_title={0} ids={1}".format(campaign.title, ids))

        self._update_prospects(ids, status=IN_PROGRESS)

    def pause_campaign(self, campaign)
        if not campaign.inprogress():
            raise Exception("Campaign already paused, title={0}".format(campaign.title))

        TaskQueue.pause_tasks(campaign_id=campaign.id)

        campaign.update_status(status=PAUSED)

    def resume_campaign(self, campaign)
        if campaign.inprogress():
            raise Exception("Campaign already resumed, title={0}".format(campaign.title))

        TaskQueue.resume_tasks(campaign_id=campaign.id)

        campaign.update_status(status=IN_PROGRESS)

        self._check_new_prospects(campaign)

    def _check_new_prospects(self, campaign):
        prospects = Prospects.get_prospects(status=NEW, campaign_id=campaign.id)
        if prospects:
            self.add_prospects(campaign, prospects)

    def _load_prospects(self, campaign, prospects):
        tasks = []

        for prospect in prospects:
            task = TaskQueue.create_task(campaign, prospect)
            tasks.append(task)

        return TaskQueue.insert_tasks(tasks)

    def _update_prospects(self, ids, status):
        Prospects.update_prospects(ids, status)

    def _setup_scheduler_data(self, campaign):
        Priority.create_priority(campaign)

