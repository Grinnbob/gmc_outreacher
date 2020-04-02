from o24.backend import db
from o24.backend import app
from o24.globals import *
from o24.backend.dashboard.models import Credentials, Campaign
from mongoengine.queryset.visitor import Q
import datetime

class Action(db.Document):
    #shared field
    action_type = db.IntField(default=0)
    data = db.DictField()
    medium = db.StringField()
    key = db.StringField()

    @classmethod
    def create_action(cls, data):
        new_action = cls()

        new_action.action_type = data.get('action_type')
        new_action.data = data.get('data')
        new_action.medium = data.get('medium')
        new_action.key = data.get('key')


        new_action._commit()
        return new_action
    
    @classmethod
    def get_by_key(cls, key):
        action = cls.objects(key=key).first()
        return action

    def _commit(self):
        self.save()
    
    def is_true(self, result):
        if self.action_type == ACTION_NONE:
            pass
            #TODO: custom action checks can be implemented
        else:
            return result.get('if_true', False)


class Funnel(db.Document):
    action = db.ReferenceField(Action)
    paramters = db.DictField()

    root = db.BooleanField(default=False)

    if_true = db.ObjectIdField(default=None)
    if_false = db.ObjectIdField(default=None)

    template = db.DictField()

    @classmethod
    def next_node(cls, current_node, result):
        next_node = None
        
        action = current_node.action

        is_true = action.is_true(result)
        if is_true:
            next_node = Funnel.objects(id=current_node.if_true).get()
        else:
            next_node = Funnel.objects(id=current_node.if_false).get()

        return next_node
        

    @classmethod
    def get_random(cls):
        funnel = cls.objects(root=True).first()
        return funnel

    @classmethod
    def get_node(cls, node_id):
        node = cls.objects(id=node_id).first()
        return node

    @classmethod
    def create_node(cls, data):
        new_funnel = cls()

        new_funnel.update_data(data)

        return new_funnel

    def update_data(self, data):

        if data.get('root', None):
            self.root = data.get('root')
        
        if data.get('action', None):
            self.action = data.get('action')

        if data.get('if_true', None):
            self.if_true = data.get('if_true')
        
        if data.get('if_false', None):
            self.if_false = data.get('if_false')

        self._commit()
        

    def _commit(self):
        self.save()

class TaskQueue(db.Document):
    current_node = db.ReferenceField(Funnel)
    
    status = db.IntField(default=0)
    
    credentials_dict = db.DictField()
    credentials_id = db.ObjectIdField()

    result_data = db.DictField()

    prospect_id = db.ObjectIdField(unique=True)
    campaing_id = db.ObjectIdField()
    
    record_type = db.IntField(default=0)
    followup_level = db.IntField(default=0)

    def switch_task(self, next_node):
        
        #init to 0
        self.current_node = next_node
        self.status = NEW
        self.result_data = {}

        self.record_type = 0
        self.followup_level = 0

        self.credentials_dict = Campaign.get_credentials(self.campaing_id, next_node)
        self.credentials_id = self.credentials_dict.get('id', None)

    @classmethod
    def get_ready(cls):
        return TaskQueue.objects(status=READY).all()

    @classmethod
    def get_execute_tasks(cls):
        
        #TODO: filter only campaigns with now in schedule_period
        #campaign_ids = Campaign.for_schedule(datetime.datetime.now())

        credential_ids = Credentials.ready_now(datetime.datetime.now())

        new_tasks = TaskQueue.objects(Q(status=NEW) & Q(credentials_id__in=credential_ids)).distinct('credentials_id').all()

        return new_tasks


    @classmethod
    def pause_tasks(cls, campaing_id):
        TaskQueue.objects(Q(campaing_id=campaing_id) & Q(status__in=TASKS_CAN_BE_PAUSED)).update(status=PAUSED)

    @classmethod
    def resume_tasks(cls, campaing_id):
        TaskQueue.objects(Q(campaing_id=campaing_id) & Q(status__in=TASKS_CAN_BE_RESUMED)).update(status=IN_PROGRESS)

    @classmethod
    def create_task(cls, campaign, prospect):
        new_task = cls()
        new_task.current_node = campaign.funnel
        
        new_task.credentials_dict = Campaign.get_credentials(campaign.id, new_task.current_node)
        new_task.credentials_id = new_task.credentials_dict.get('id', None)

        new_task.prospect_id = prospect.id
        new_task.campaing_id = campaign.id

        return new_task

    @classmethod
    def update_tasks(cls, tasks):
        if not tasks:
            return None
        
        TaskQueue.objects.update(tasks)

    @classmethod
    def insert_tasks(cls, tasks):
        if not tasks:
            return None
        
        return TaskQueue.objects.insert(tasks, load_bulk=True)