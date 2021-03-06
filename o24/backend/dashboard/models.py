from o24.backend import db
from o24.backend import app

from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
from math import ceil

import uuid
from mongoengine.queryset.visitor import Q
import json
import traceback

from werkzeug.security import check_password_hash, generate_password_hash
from o24.globals import *
import o24.config as config

from passlib.context import CryptContext

import o24.backend.models.shared as shared
import o24.backend.scheduler.scheduler as scheduler

from bson import ObjectId
from bson.json_util import dumps as bson_dumps
from o24.backend.utils.filter_data import *
from o24.backend.utils.helpers import template_key_dict 
from o24.backend.dashboard.serializers import JSCampaignData
import string
import random
from random import randrange
from urllib.parse import unquote, urlparse
import io
import csv

def generate_invite_code(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class User(db.Document):
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(nullable=False)

    enrich_credits = db.IntField(default=0)

    active = db.BooleanField(default=True)
    current_oauth_state = db.StringField()

    role = db.StringField(default='user')

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    invite_code = db.StringField(default='')
    invited_by = db.StringField(default='')

    def when_created(self):
        #Create special-medium
        exist = Credentials.objects(owner=self.id, medium='special-medium').first()
        if not exist:
            exist = Credentials.create_credentials(owner=self.id, 
                                                    new_data={}, 
                                                    medium='special-medium')

        return True

    def _init_user(self, 
                    email=None, 
                    password=None, 
                    invited_by='', 
                    invite_code=''):

        if not email or not password:
            raise Exception("Email or password can't be empty")

        self.email = email
        try:
            self.password = generate_password_hash(password)
        except:
            raise Exception("Week password - try another, 8 symbols minimum")

        if not invite_code:
            self.invite_code = generate_invite_code()
        else:
            self.invite_code = invite_code

        self.invited_by = invited_by

    @classmethod
    def get_by_state(cls, state):
        return cls.objects(current_oauth_state=state).first()

    @classmethod
    def register(cls, user_data):
        email = user_data.get_email()
        password = user_data.get_password()
        repeat_password = user_data.get_repeat_password()
        invite_code = user_data.get_invite_code()

        exist = cls.objects(email=email).first()
        if exist:
            raise Exception("User with this email already exists")

        if not email:
            raise Exception("Email can't be empty")

        if not password:
            raise Exception("Password can't be empty")
        
        if password != repeat_password:
            raise Exception("Passwords should be equal")

        if not invite_code:
            raise Exception("You need an Invite code to register")

        ref = cls.objects(invite_code=invite_code).first()
        if not ref:
            raise Exception("Unvalid invite code")
            
        new_user = cls()
        new_user._init_user(
            email=email,
            password=password,
            invited_by=invite_code
        )

        return new_user


    @classmethod
    def authenticate(cls, user_data):
        email = user_data.get_email()
        password = user_data.get_password()
        
        if not email or not password:
            error = "Can't be empty: email: {0} password:{1}".format(email, password)
            raise Exception(error)

        user = cls.objects(email=email).first()
        if not user:
            error = "No user with email:{0}, sign up first".format(email)
            raise Exception(error)
        
        if not check_password_hash(user.password, password):
            raise Exception("Incorrect password")

        return user


    @classmethod
    def create_user(cls, data):
        new_user = cls()
        new_user._init_user(
            email=data.get('email'),
            password=data.get('password'),
            invited_by=data.get('invited_by', ''),
            invite_code=data.get('invite_code', '')
        )

        enrich_credits = int(data.get('enrich_credits', 0))
        if enrich_credits:
            new_user.enrich_credits = enrich_credits

        new_user.role = data.get('role', 'user')
        new_user._commit()
        return new_user
    
    @classmethod
    def get_user(cls, email):
        user = cls.objects(email=email).first()
        return user

    def change_password(self, old_password, new_password):
        if not old_password or not new_password:
            raise Exception("Password can't be empty")

        if not check_password_hash(self.password, old_password):
            raise Exception("Incorrect password")
        
        self.password = generate_password_hash(new_password)
        self._commit()

    def admin_change_password(self, new_password):
        self.password = generate_password_hash(new_password)
        self._commit()

    def new_oauth_state(self):
        self.current_oauth_state = self._generate_ouath_state()
        self._commit()
        
        return self.current_oauth_state

    def withdraw_credits(self, amount):
        self.enrich_credits = self.enrich_credits - amount
        self._commit()

        return self.enrich_credits

    def get_credits(self):
        return self.enrich_credits

    def _generate_ouath_state(self):
        state = uuid.uuid4().hex

        return state


    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

    def __repr__(self):
        return '<User %r>' % (self.email)

class FormSession(db.Document):
    owner = db.ReferenceField(User, reverse_delete_rule=1)
    form_name = db.StringField()

    data = db.DictField()

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

class BlackList(db.Document):
    owner = db.ReferenceField(User, reverse_delete_rule=1)

    emails = db.StringField()
    domains = db.StringField()
    linkedin = db.StringField()

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    @classmethod
    def async_list(cls, owner_id):
        exist = cls.objects(owner=owner_id).first()
        if not exist:
            return {}
        
        return exist.to_json()

    @classmethod
    def get_black_list(cls, owner_id):
        exist = cls.objects(owner=owner_id).first()
        if not exist:
            exist = cls(owner=owner_id)
            exist._commit(_reload=True)
        
        return exist
    
    def _serialize_entities(self, _emails, _domains, _linkedin):
        self.emails = json.dumps(_emails, indent=4, sort_keys=True, default=str)
        self.domains = json.dumps(_domains, indent=4, sort_keys=True, default=str)
        self.linkedin = json.dumps(_linkedin, indent=4, sort_keys=True, default=str)

    def _deserialize_entities(self):
        _emails = {}
        _domains = {}
        _linkedin = {}

        if self.emails:
            _emails = json.loads(self.emails)
        
        if self.domains:
            _domains = json.loads(self.domains)

        if self.linkedin:
            _linkedin = json.loads(self.linkedin)

        return _emails, _domains, _linkedin

    def remove_entities(self, entities):
        _emails, _domains, _linkedin = self._deserialize_entities()
        for key in entities:
            _emails.pop(key, None)
            _domains.pop(key, None)
            _linkedin.pop(key, None)

        self._serialize_entities(_emails=_emails,
                                _domains=_domains,
                                _linkedin=_linkedin)

        self._commit()
        return

    def add_list(self, entities):
        _emails, _domains, _linkedin = self._deserialize_entities()

        emails = entities.get('emails', None)
        if emails:
            for email in emails:
                if '@' not in email:
                    continue
                email = email.replace(" ","")
                if email not in _emails.keys():
                    _emails[email] = pytz.utc.localize(datetime.utcnow())
            
        domains = entities.get('domains', None)
        if domains:
            for domain in domains:
                domain = domain.replace(" ","")
                if domain not in _domains.keys():
                    _domains[domain] = pytz.utc.localize(datetime.utcnow())
        
        linkedin_accounts = entities.get('linkedin', None)
        if linkedin_accounts:
            for li_acc in linkedin_accounts:
                li_acc = li_acc.replace(" ","")
                li_acc = urlparse(li_acc).path
                if li_acc:
                    li_acc = li_acc.strip('/')
                    if li_acc not in _linkedin.keys():
                        _linkedin[li_acc] = pytz.utc.localize(datetime.utcnow())
        
        self._serialize_entities(_emails=_emails,
                                _domains=_domains,
                                _linkedin=_linkedin)

        self._commit()

    @classmethod
    def is_listed_email(cls, owner_id, email):
        black_list = cls.objects(owner=owner_id).first()
        if not black_list:
            return False

        _emails, _domains, _linkedin = black_list._deserialize_entities()

        stripped = email.replace(" ", "")
        if stripped in _emails.keys():
            return True

        email_domain = stripped.split('@')
        if len(email_domain) > 1:
            email_domain = email_domain[1]
            if email_domain in _domains.keys():
                return True

        return False

    @classmethod
    def is_listed_linkedin(cls, owner_id, account):
        black_list = cls.objects(owner=owner_id).first()
        if not black_list:
            return False

        _emails, _domains, _linkedin = black_list._deserialize_entities()

        stripped = account.replace(" ", "")
        path = urlparse(stripped).path
        if path:
            path = path.strip('/')
            if path in _linkedin.keys():
                return True

        return False


    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

#### Menu: Outreach Accounts ####
#### Store data to access external accounts
class Credentials(db.Document):
    SHOWED_MEDIUM = ['linkedin', 'email']

    owner = db.ReferenceField(User, reverse_delete_rule=1)
    
    # 0 - Fresh or just created
    # 1 - Refreshed (need to update all tasks)
    # -1 - Failed
    status = db.IntField(default=0)
    error_message = db.StringField(default='')
    ack = db.IntField(default=0)

    medium = db.StringField()
    modification = db.StringField()

    data = db.DictField()
    
    day_first_action = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))
    last_action = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))
    next_action = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))

    limits = db.DictField()
    warmup_limits = db.DictField()
    current_actions_count = db.DictField()

    current_daily_counter = db.IntField(default=0)
    warmup_active = db.BooleanField(default=True) 

    #FOR test purpose only
    test_title = db.StringField(default='')

    def setup_limits(self, medium, modification, _commit=False):
        if medium in NO_LIMITS_MEDIUMS:
            return True

        medium_limits = LIMITS_BASED_ON_MEDIUM.get(medium, '')
        if not medium_limits:
            raise Exception("setup_limits ERROR: Unknown medium={0}".format(medium))
        
        modification_limits = medium_limits.get(modification, '')
        if not modification_limits:
            raise Exception("setup_limits ERROR: Unknown modification={0} for medium={1}".format(modification, medium))
        
        self.limits = modification_limits.get('limits')
        self.warmup_limits = modification_limits.get('warmup')

        account_maximum = self.limits.get('account_maximum')

        if _commit:
            self._commit()

    def update_modification(self, modification, _commit=False):
        if self.medium in NO_LIMITS_MEDIUMS:
            return True

        if self.modification == modification:
            return

        medium_limits = LIMITS_BASED_ON_MEDIUM.get(self.medium, '')
        if not medium_limits:
            raise Exception("setup_limits ERROR: Unknown medium={0}".format(self.medium))
        
        modification_limits = medium_limits.get(modification, '')
        if not modification_limits:
            raise Exception("setup_limits ERROR: Unknown modification={0}".format(modification))
        
        self.limits = modification_limits.get('limits')
        self.warmup_limits = modification_limits.get('warmup')

        #TODO: remove it, need to fix frontend
        self.modification = modification

        if _commit:
            self._commit()

    def update_account_maximum(self, _commit=False):
        if self.medium in NO_LIMITS_MEDIUMS:
            return False
        
        medium_limits = LIMITS_BASED_ON_MEDIUM.get(self.medium, '')
        if not medium_limits:
            raise Exception("update_account_maximum ERROR: Unknown medium={0}".format(self.medium))
        
        modification_limits = medium_limits.get(self.modification, '')
        if not modification_limits:
            raise Exception("update_account_maximum ERROR: Unknown modification={0}".format(self.modification))
        
        account_maximum = modification_limits.get('limits').get('account_maximum')
        warmup_account_maximum_default = modification_limits.get('warmup').get('account_maximum')

        if _commit:
            self._commit()

    def check_limits(self, action_key):
        # True - if we have limits
        # False - if we don't have limits
        # None - Unlimited
        # Here is the sequence to check
        # 1. Is medium unlimitted?
        # 2. Is action_key unlimitted?
        # 3. Do we exceed account maximum?
        # 4. Do we exceed action_key maximum?

        if self.medium in NO_LIMITS_MEDIUMS:
            return None
           
        #Do we have limits for this action_key?
        action_key_maximum = self.warmup_limits.get(action_key, None)
        if action_key_maximum is None:
            return None

        current_action_key_counter = self.current_actions_count.get(action_key, 0)
        if current_action_key_counter > action_key_maximum:
            return False

        #Do we exceed account_maximum?
        account_maximum = self.warmup_limits.get('account_maximum', None)
        if account_maximum is None:
            print("NEVER HAPPENED: there is no account_maximum for warmup_limits for credentials_id={0}".format(self.id))
            return False

        if self.current_daily_counter > account_maximum:
            return False


        return True

    def get_limits(self):
        res = {
            'maximum' : self.limits,
            'current' : self.warmup_limits
        }

        return json.dumps(res)

    def update_limits(self, limits_data):
        
        for action, count in self.warmup_limits.items():
            if action in ['interval_sec', 'increase', 'days_inactivity']:
                continue 

            new_value = limits_data.get_field(field=action, default=None)
            max_possible = self.limits.get(action, 0)

            if new_value is not None:
                if new_value <= max_possible:
                    self.warmup_limits[action] = new_value

                    #account_maximum not used by email right now, maybe in the future
                    if action == EMAIL_SEND_MESSAGE_ACTION:
                        self.warmup_limits['account_maximum'] = new_value

        self._commit()

        return self.warmup_limits

    @classmethod
    def ready_ids(cls, utc_now):
        #ids = [p.get('_id') for p in cls.objects(next_action__lte=utc_now).only('id').all().as_pymongo()]
        ids = cls.objects(next_action__lte=utc_now, status=0).distinct('id')
        return ids

    @classmethod
    def create_credentials(cls, owner, new_data, medium, modification=None):
        exist = None

        #hash password
        #password = new_data.get('password', '')
        #if password:
        #    new_data['password'] = encode_password(password)

        account = new_data.get('account', '')
        if account:
            exist = Credentials.objects(owner=owner, data__account=account).first()

        if not exist:
            exist = cls()

        if modification:
            exist.modification = modification

        exist.setup_limits(medium=medium, 
                            modification=modification)

        exist.owner = owner
        exist.medium = medium
        exist.data = new_data
        
        if medium in ACTIVATED_MEDIUMS:
            exist.status = 1
        else:
            exist.status = 0
        
        exist._commit(_reload=True)

        return exist
     

    def safe_delete_credentials(self):
        campaign_assigned = Campaign.objects(owner=self.owner, credentials__in=[self.id]).first()
        if campaign_assigned:
            account = self.data.get('account', '')
            error = "Can't delete credentials for account:{0} - you have campaign assigned, delete campaign first".format(account)
            raise Exception(error)
        
        return self.delete()


    @classmethod
    def get_credentials(cls, user_id, medium=None, sender=None):
        if medium is not None:
            return cls.objects(owner=user_id, medium=medium).first()

        if sender is not None:
            return cls.objects(owner=user_id, data__sender=sender).first()

        return None

    @classmethod
    def admin_async_credentials(cls):
        db_query = cls.objects(medium__in=cls.SHOWED_MEDIUM)

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "user",
                "localField" : "owner",
                "foreignField" : "_id",
                "as" : "owner"
            }},
            { "$unwind" : { "path" : "$owner", "preserveNullAndEmptyArrays": True }},
        ]

        credentials = list(db_query.aggregate(*pipeline))

        results = bson_dumps(credentials)

        return results

    @classmethod
    def async_credentials(cls, owner, page=None, medium=None, per_page=config.CREDENTIALS_PER_PAGE, active_only=False):
        if page and page <= 1:
            page = 1

        query = {
            'owner' : owner
        }
        if active_only:
            query['status'] = 1

        if medium:
            query['medium'] = medium
        
        db_query = cls.objects(__raw__=query, medium__in=cls.SHOWED_MEDIUM). \
                    only('id', 'data', 'status', 'error_message', 'medium', 'modification', 'warmup_active', 'last_action', 'next_action', 'current_daily_counter')
        
        total = db_query.count()
        results = []
        if page is not None:
            results = db_query.skip(per_page * (page-1)).limit(per_page).order_by('status')
        else:
            results = db_query.order_by('status')
        
        if results:
            results = results.to_json()

        return (total, results)


    @classmethod
    def list_credentials(cls, credential_ids):
        return cls.objects(id__in=credential_ids)

    @classmethod
    def update_credentials(cls, arr):
        if not arr:
            return None

        for e in arr:
            e._commit()
        #cls.objects.update(arr)

    def get_account(self):
        return self.data['account']

    def get_data(self):
        return self.data
    
    def get_medium(self):
        return self.medium

    def _refresh_limits(self, _commit=False):
        self.current_daily_counter = 0
        self.current_actions_count = {}

        if _commit:
            self._commit()

    def _increase_action_counter(self, action_key):
        now = pytz.utc.localize(datetime.utcnow())

        self.current_daily_counter = self.current_daily_counter + 1
        self.last_action = self.next_action
        
        account_maximum = self.warmup_limits.get('account_maximum')
        interval = self.warmup_limits.get('interval_sec')

        if self.current_daily_counter >= account_maximum:
            #switch action to the next day
            self.next_action = now + timedelta(seconds=LIMITS_24_PERIOD_SECS)
            self._refresh_limits()
            self.warmup()
        else:
            random_interval = randrange(interval, interval * RANDOM_INTERVAL_MAX)
            self.next_action = now + timedelta(seconds=random_interval)        

        #INCREASE action_counter
        current_counter = self.current_actions_count.get(action_key, 0)
        
        new_counter = current_counter + 1
        self.current_actions_count[action_key] = new_counter

    def _check_inactivity_days(self):
        now = pytz.utc.localize(datetime.utcnow())
        
        diff = now - self.last_action
        diff_days = diff.days

        max_inactivity_days = self.warmup_limits.get('days_inactivity')
        if diff_days > max_inactivity_days:
            self.warmup_refresh()

    def _check_day_changed(self):
        now = pytz.utc.localize(datetime.utcnow())

        diff = now - self.day_first_action
        diff_seconds = diff.seconds
        if diff_seconds < 0:
            diff_seconds = diff_seconds * -1
        
        if diff_seconds >= LIMITS_24_PERIOD_SECS:
            self.day_first_action = now
            self._refresh_limits()

        return

    def change_limits(self, action_key):
        has_limits = self.check_limits(action_key=action_key)

        #None - action_key or medium is unlimited
        if has_limits is None:
            return True

        # If 24-hour period ended all limits are refreshed
        self._check_inactivity_days()
        self._check_day_changed()


        # we don't have limits left for this action_key
        if has_limits == False:
            return False

        #We have limits left need to:
        # 1. Increase daily_counter (total actions on this account)
        # 2. Increase counter for action_key
        # 3. Change next_action if exceeded:
             # we have exceed account_maximum, need to move to 24 hour in the future
             # warmup account
        # 4. Change next_action to interval if exceeded
        self._increase_action_counter(action_key=action_key)

        return True

    def _inc_next_action(seconds, _commit=True):
        now = pytz.utc.localize(datetime.utcnow())

        self.next_action = now + timedelta(seconds=seconds)
        self.current_daily_counter = 0
        
        if _commit:
            self._commit()

    def _check_for_duplicates(self, data):
        #check duplicates:
        account = data.get('account', '')
        if account:
            exist = Credentials.objects(owner=self.owner, data__account=account, id__ne=self.id).first()
            if exist:
                error = "Credentials duplicate error for account: {0}".format(account)
                raise Exception(error)

    def safe_update_credentials(self, credentials_data, _reload=False):
        modification = credentials_data.get_modification()
        if modification and self.modification != modification:
            self.update_modification(modification=modification)

        warmup_active = credentials_data.get_field(field='warmup_active', default=None)
        if not warmup_active:
            self.warmup_active = False
        else:
            self.warmup_active = True
        
        if self.medium != 'email':
            data = credentials_data.get_data()
            
            if data:
                #TODO: Check data serialization
                if data.get('expiry', None) is not None:
                    data.pop('expiry', None) 

                self.update_data(new_data=data, _commit=False)
        
        self._commit(_reload=_reload)

    def update_data(self, new_data, _commit=True):
        if not isinstance(new_data, dict):
            raise Exception("Can't update_data, new_data is not dict object")
        
        if not new_data:
            return 0

        self._check_for_duplicates(new_data)
        for key, val in new_data.items():
            if val is not None:
                self.data[key] = val
        
        if _commit:
            self._commit()
    
    def error(self, error=''):
        self.error_message = error
        self.status = -1

        self._commit()

    def resolved(self, _reload=False):
        self.error_message = ''
        self.status = 1
        
        self._commit(_reload=_reload)

    def get_auth_credentials(self):
        credentials = self.data.get('credentials', None)
        expiry = self.data.get('expiry', None)
        return credentials, expiry
        
    def update_auth_credentials(self, new_credentials, expiry):
        self.data['credentials'] = new_credentials
        self.data['expiry'] = expiry

        self._commit()

    def change_status(self, status):
        self.status = status
        self._commit()

    def warmup_refresh(self, _commit=False):
        if self.medium in NO_LIMITS_MEDIUMS:
            return True

        medium_limits = LIMITS_BASED_ON_MEDIUM.get(self.medium, '')
        if not medium_limits:
            raise Exception("warmup_refresh ERROR: Unknown medium={0}".format(self.medium))
        
        modification_limits = medium_limits.get(self.modification, '')
        if not modification_limits:
            raise Exception("warmup_refresh ERROR: Unknown modification={0}".format(self.modification))
        
        self.warmup_limits = modification_limits.get('warmup')

        if _commit:
            self._commit()


    def warmup(self, _commit=False):
        if not self.warmup_active:
            return

        if not self.warmup_limits:
            raise Exception("NEVER HAPPENED: there is no warmup_limits for cr_id={0}".format(self.id))
        
        increase = self.warmup_limits.get('increase')
        for action, counter in self.warmup_limits.items():
            if action in WORKAROUND_PASS:
                continue

            max_counter = self.limits.get(action)
            next_counter = ceil(counter * increase)

            if next_counter > max_counter:
                self.warmup_limits[action] = max_counter
            else:
                self.warmup_limits[action] = next_counter

        if _commit:
            self._commit()


    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()


#### Menu: Teams ####
#### Manage teams
class Team(db.Document):
    admin = db.ReferenceField(User, reverse_delete_rule=1)
    
    title = db.StringField()
    members = db.ListField(db.ReferenceField(User, reverse_delete_rule=1))

    @classmethod
    def create_team(cls, data):
        new_team = cls()

        new_team.admin = data.get('admin')
        new_team.title = data.get('title')
        new_team.members = data.get('members')

        new_team._commit()

        return new_team

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()

class Campaign(db.Document):
    RESTRICTED_SET_FIELDS = [
        'owner',
        'id',
        '_id',
        'status',
        'last_action',
        'next_action',
        'created'
    ]

    CAN_BE_NULL = ['from_hour', 'to_hour', 'from_minutes', 'to_minutes', 'status']

    @classmethod
    def get_create_fields(cls):
        return cls._fields.keys()

    owner = db.ReferenceField(User, reverse_delete_rule=1, required=True)
    # 0 - created
    # 1 - in progress
    # 2 - paused
    # 11 - archived (deleted)
    # 12 - draft
    status = db.IntField(default=0)
    campaign_type = db.IntField(default=0)
    message = db.StringField(default='')

    custom_delays = db.DictField()
    tracking_events = db.DictField(default=DEAFULT_TRACKING_EVENTS)

    title = db.StringField(required=True)

    credentials = db.ListField(db.ReferenceField(Credentials, reverse_delete_rule=1))

    funnel = db.ReferenceField(shared.Funnel, reverse_delete_rule=1)

    #in case it's a fork campaign
    fork_from = db.ObjectIdField()
    
    #get from timeTable
    sending_days = db.DictField(default=DEFAULT_SENDING_DAYS)
    from_hour = db.IntField(default=DEFAULT_FROM_HOUR)
    from_minutes = db.IntField(default=0)
    to_hour = db.IntField(default=DEFAULT_TO_HOUR)
    to_minutes = db.IntField(default=0)
    time_zone = db.DictField(default=DEFAULT_TIME_ZONE)

    templates = db.DictField()

    data = db.DictField()
    cache = db.DictField()

    last_action = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))
    next_action = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    @classmethod
    def admin_async_campaigns_list(cls, page=None, per_page=config.CAMPAIGNS_PER_PAGE):
        if page and page <= 1:
            page = 1

        db_query = cls.objects()
                
        total = db_query.count()

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "user",
                "localField" : "owner",
                "foreignField" : "_id",
                "as" : "user"
            }},
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "credentials",
                "foreignField" : "_id",
                "as" : "credentials"
            }},
            {"$lookup" : {
                "from" : "funnel",
                "localField" : "funnel",
                "foreignField" : "_id",
                "as" : "funnel"
            }},
            { "$unwind" : { "path" : "$funnel", "preserveNullAndEmptyArrays": True }},
            { "$project" : { 
                'status' : 1,
                'data' : 1,
                'title' : 1,
                'credentials' : 1,
                'user' : 1,
                'funnel' : 1,
                'message' : 1,
                'campaign_type' : 1
            }}
        ]

        campaigns = []
        if page is not None:
            campaigns = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline))
        else:
            campaigns = list(db_query.order_by('-created').aggregate(*pipeline))

        results = bson_dumps(campaigns)

        return (total, results)


    @classmethod
    def async_campaigns_list(cls, owner, page=None, campaign_types=[0], per_page=config.CAMPAIGNS_PER_PAGE):
        if page and page <= 1:
            page = 1

        db_query = cls.objects(owner=owner, campaign_type__in=campaign_types)
                
        total = db_query.count()

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "credentials",
                "localField" : "credentials",
                "foreignField" : "_id",
                "as" : "credentials"
            }},
            {"$lookup" : {
                "from" : "funnel",
                "localField" : "funnel",
                "foreignField" : "_id",
                "as" : "funnel"
            }},
            { "$unwind" : { "path" : "$funnel", "preserveNullAndEmptyArrays": True }},
            { "$project" : { 
                'status' : 1,
                'data' : 1,
                'title' : 1,
                'credentials' : 1,
                'funnel' : 1,
                'message' : 1,
                'campaign_type' : 1
            }}
        ]

        campaigns = []
        if page is not None:
            campaigns = list(db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline))
        else:
            campaigns = list(db_query.order_by('-created').aggregate(*pipeline))

        results = bson_dumps(campaigns)

        return (total, results)

    @classmethod
    def get_campaign(cls, owner=None, id=None, title=None):
        
        campaign = None
        if owner:
            campaign = cls.objects(owner=owner, id=id).first()
        if title:
            campaign = cls.objects(title=title).first()
        elif id:
            campaign = cls.objects(id=id).first()

        return campaign

    @classmethod
    def create_campaign(cls, data, owner):
        new_campaign = cls()

        new_campaign.owner = owner

        new_campaign.title = data.get('title', '')
        new_campaign.credentials = data.get('credentials')
        new_campaign.funnel = data.get('funnel')

        if data.get('templates', ''):
            new_campaign.templates = data.get('templates')
        
        if data.get('time_table', ''):
            timeTable = data.get('time_table')
            new_campaign.sending_days = timeTable.get('sending_days')
            new_campaign.from_hour = timeTable.get('from_hour')
            new_campaign.to_hour = timeTable.get('to_hour')
            new_campaign.time_zone = timeTable.get('time_zone')


        new_campaign.data = data.get('data')

        new_campaign.status = NEW
    
        new_campaign.set_next_action_on_edit(_commit=False)
        new_campaign._commit()
        return new_campaign
    
    @classmethod
    def get_credentials_id(cls, campaign_id, funnel_node):
        campaign = cls.objects(id=campaign_id).get()

        medium = funnel_node.action.medium

        if medium == 'special-medium':
            return campaign.get_special_medium_id()
        
        for c in campaign.credentials:
            if c.medium == medium:
                return c.id
        
        return None
                
    @classmethod
    def update_campaigns(cls, campaigns):
        if not campaigns:
            return None

        for c in campaigns:
            c._commit()

    #show which contacts need to be in prospect to execute this campaign 
    def need_contacts(self):
        return self.funnel.list_of_contacts()

    def get_special_medium_id(self):
        owner_id = self.owner.id

        special_medium = Credentials.objects(owner=owner_id, medium='special-medium').first()
        if not special_medium:
            return None
        
        return special_medium.id

    #Only for LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE
    def get_parsed_list(self):
        if self.campaign_type != LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE:
            return None
        
        if not self.fork_from:
            return None

        forked_from_campaign = Campaign.objects(id=self.fork_from).first()
        if not forked_from_campaign:
            return None
        
        list_id = forked_from_campaign.data.get('list_id', None)
        if not list_id:
            return None
        
        return list_id

    def parsing_switch(self, next_url):
        is_finished = False

        current_search_url = self.data.get('search_url', None)
        if current_search_url and current_search_url == next_url:
            return is_finished

        if self.campaign_type != LINKEDIN_PARSING_CAMPAIGN_TYPE:
            raise Exception("parsing_switch wrong campaign_type={0}".format(self.campaign_type))
        
        pages_total = int(self.data.get('total_pages', 0))
        interval_pages = int(self.data.get('interval_pages', 0))

        pages_done = int(self.data.get('pages_done', 0))
        pages_done = pages_done + interval_pages

        #UPDATE DATA - will be pass to handler through input_data
        if self.data.get('start_url', None) is None:
            self.data['start_url'] = self.data.get('search_url', '')

        self.data['search_url'] = next_url
        self.data['pages_done'] = pages_done

        if pages_done >= pages_total:
            is_finished = True

        self._commit()

        return is_finished

    def set_linkedin_enrichment_funnel(self):
        funnel_id = shared.Funnel.get_linkedin_enrichment_funnel_id()
        self.funnel = funnel_id
        self._commit()


    def set_linkedin_parsing_funnel(self):
        funnel_id = shared.Funnel.get_linkedin_parsing_funnel_id()
        self.funnel = funnel_id
        self._commit()

    def valid_funnel(self):
        if self.funnel == None:
            return False
        
        return True

    def get_template_data(self, template_key, medium):
        templates_for_medium = self.templates.get(medium, '')
        
        #only plain supported for linkedin
        if medium == 'linkedin':
            templates_for_medium = self.templates.get('linkedin_plain', '')

        if not templates_for_medium:
            return {}
        
        template_data = templates_for_medium.get(template_key, {})
        
        #check if plain exist
        plain = self.templates.get('plain', None)
        if plain:
            plain_for_key = plain.get(template_key, None)
            if plain_for_key:
                template_data['plain'] = plain_for_key

        return template_data

    def get_node_template(self, template_key, medium):
        if not template_key:
            return ''
        
        if not medium:
            raise Exception("ERROR: get_node_template, medium can't be empty")
        
        templates_for_medium = self.templates.get(medium, '')
        if not templates_for_medium:
            return ''
        
        template = templates_for_medium.get(template_key, '')
        return template

    def _convert_campaign_interval_to_utc(self, hour, minute):
        campaign_tz_title = self.time_zone.get('value', None)
        if campaign_tz_title is None:
            raise Exception("Wrong time_zone format for campaign.id={0}".format(self.id))
        campaign_tz = timezone(campaign_tz_title)

        now = pytz.utc.localize(datetime.utcnow())
        tz_campaign_time = datetime(year=now.year,
                                month=now.month,
                                day=now.day,
                                hour=hour,
                                minute=minute,
                                tzinfo=campaign_tz)

        utc_campaign_time = tz_campaign_time.astimezone(pytz.utc)
        return utc_campaign_time

    #convert from sending time from CAMPAIGN time zone to UTC
    def get_from_interval_in_utc(self):
        return self._convert_campaign_interval_to_utc(hour=self.from_hour,
                                                        minute=self.from_minutes)

    #convert to sending time from CAMPAIGN time zone to UTC
    def get_to_interval_in_utc(self):
        return self._convert_campaign_interval_to_utc(hour=self.to_hour,
                                                        minute=self.to_minutes)

    def set_next_action_on_edit(self, _commit=True):
        #If edits happened when the day limit exceed
        now = pytz.utc.localize(datetime.utcnow())

        #we get from sending time in UTC 
        #next_action - is offset-aware datetimes
        next_action = self.get_from_interval_in_utc()
        start_day = next_action.weekday()

        to_interval = self.get_to_interval_in_utc()
        too_late = now.hour >= to_interval.hour

        days_delta = 0
        if too_late or not self.sending_days.get(str(start_day)):
            days_delta = self.days_delta(start_day)

        self.next_action = next_action + timedelta(days=days_delta)

        if _commit:
            self._commit()
        
        return self.next_action   

    def change_limits(self):
        now = pytz.utc.localize(datetime.utcnow())

        current_hour = now.hour
        current_day = now.day
        
        utc_to_interval = self.get_to_interval_in_utc()
        utc_to_hour = utc_to_interval.hour

        if current_hour >= utc_to_hour:
            self.last_action = self.next_action

            days_delta = self.days_delta(current_day)

            next_t = now + timedelta(days=days_delta)
            self.next_action = next_t.replace(hour=self.from_hour, minutes=0)
    

    def days_delta(self, current_day):
        delta = 1
        next_day = current_day + 1
        a = self.sending_days

        for i in range(6):
            if next_day > 6:
                next_day = 0

            if a.get(str(next_day)):
                break

            delta = delta + 1
            next_day = next_day + 1

        return delta

    def _allow_no_prospects(self):
        if self.campaign_type == LINKEDIN_PARSING_CAMPAIGN_TYPE:
            return True

        return False

    def _safe_pause(self, message=''):
        self.message = message

        self.update_status(status=PAUSED)

    def _safe_start(self):
        if self.inprogress():
            raise Exception("Starting error: campaign already in progress")
        
        if not self.funnel:
            raise Exception("Starting error: there is not selected funnel for campaign_id:{0}".format(self.id))
        
        if not self._allow_no_prospects():
            has_prospects = Prospects.get_prospects(campaign_id=self.id)
            if not has_prospects:
                raise Exception("Starting error: There is no assigned prospects for this campaign")

        self.update_status(status=IN_PROGRESS)
        self.message = ''

    def _validate_campaign_data(self, owner, campaign_data, changed_fields):

        if 'title' in changed_fields:
            title = campaign_data.title()
            if not title:
                raise Exception("Title can't be empty")
            
            exist = None
            if self.id is not None:
                exist = Campaign.objects(owner=owner, id__ne=self.id, title=title).first()
            else:
                exist = Campaign.objects(owner=owner, title=title).first()

            if exist:
                raise Exception("Campaign with this title already exist")


    def _async_set_field(self, field_name, val):
        if field_name == 'title':
            if not val:
                raise Exception("Campaign title can't be empty")

            self.title = val
        else:
            setattr(self, field_name, val)

    def update_data(self, new_data, _commit=True):
        for k,v in new_data.items():
            self.data[k] = v
        if _commit:
            self._commit()

    def async_edit(self, owner, campaign_data, edit_fields, restricted_fields=None):
        if not restricted_fields:
            restricted_fields = self.RESTRICTED_SET_FIELDS

        self._validate_campaign_data(owner=owner, campaign_data=campaign_data, changed_fields=edit_fields)

        for field in edit_fields:
            if field in restricted_fields:
                continue

            val = campaign_data.get_field(field)
            if val:
                if field == 'data':
                    self.update_data(new_data=val, _commit=False)
                else:
                    self._async_set_field(field_name=field, val=val)
            elif field in self.CAN_BE_NULL:
                self._async_set_field(field_name=field, val=val)
        
        self.set_next_action_on_edit(_commit=False)

        self._commit(_reload=True)
        return True

    @classmethod
    def async_create(cls, owner, campaign_data, create_fields, campaign_type=0, restricted_fields=None):
        if not restricted_fields:
            restricted_fields = cls.RESTRICTED_SET_FIELDS

        new_campaign = cls()
        new_campaign.owner = owner
        new_campaign.campaign_type = campaign_type
        
        new_campaign._validate_campaign_data(owner=owner, campaign_data=campaign_data, changed_fields=create_fields)

        for field in create_fields:
            if field in restricted_fields:
                continue
    
            val = campaign_data.get_field(field)
            if val:
                new_campaign._async_set_field(field_name=field, val=val)
            elif field in cls.CAN_BE_NULL:
                new_campaign._async_set_field(field_name=field, val=val)

        new_campaign.set_next_action_on_edit(_commit=False)
        new_campaign._commit(_reload=True)
        return new_campaign


    def inprogress(self):
        if self.status == 1:
            return True
        
        return False

    def get_tracking_events(self):
        if not self.tracking_events:
            return {}
        
        return self.tracking_events

    #Saved in days
    #Convert to seconds
    def get_delay(self, template_key):
        if not self.templates:
            return None
        
        #Try email medium
        email_templates = self.templates.get('email', {})

        email_template = email_templates.get(template_key, {})
        if email_template:
            delay_days = email_template.get('interval', None)
            if delay_days is not None:
                delay = delay_days * DAY_TO_SECONDS
                return delay
        
        #Try linkedin medium
        linkedin_templates = self.templates.get('linkedin', {})
        
        linkedin_template = linkedin_templates.get(template_key, {})
        if linkedin_template:
            delay_days = linkedin_template.get('interval', None)
            if delay_days is not None:
                delay = delay_days * DAY_TO_SECONDS
                return delay

        #Try custom delays
        if self.custom_delays:
            delay_days = self.custom_delays.get(template_key, None)
            if delay_days is not None:
                delay = delay_days * DAY_TO_SECONDS
                return delay

        return None

    def get_funnel_type(self):
        return self.funnel.funnel_type

    def get_data(self):
        return self.data

    def get_list_id(self):
        if not self.data:
            return None

        return self.data.get('list_id', None)
    
    def add_data_value(self, key, value):
        self.data[key] = value
        self._commit()

    def get_update_existing(self):
        if not self.data:
            return False

        return self.data.get('update_existing', False)

    def get_owner_id(self):
        if not self.owner:
            return None
        
        return self.owner.id

    def update_status(self, status):
        self.status = status
        self._commit()

    def fork_linkedin_enrichment_campaign(self):
        if self.campaign_type != LINKEDIN_PARSING_CAMPAIGN_TYPE:
            raise Exception("fork_linkedin_enrichment_campaign ERROR: wrong campaign_type".format(self.campaign_type))
        
        new_campaign = Campaign()
        new_campaign.fork_from = self.id

        new_campaign.title = "In-depth linkedin profile parsing for {0}".format(self.title)
        new_campaign.owner = self.owner

        new_campaign.credentials = self.credentials

        new_campaign.funnel = shared.Funnel.get_linkedin_enrichment_funnel_id()

        if self.custom_delays:
            new_campaign.custom_delays = self.custom_delays
        
        new_campaign.sending_days = self.sending_days
        new_campaign.from_hour = self.from_hour
        new_campaign.to_hour = self.to_hour

        new_campaign.from_minutes = self.from_minutes
        new_campaign.to_minutes = self.to_minutes

        new_campaign.time_zone = self.time_zone

        new_campaign.status = NEW
        new_campaign.campaign_type = LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE

        new_campaign._commit(_reload=True)

        return new_campaign

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()




class ProspectsList(db.Document):
    owner = db.ReferenceField(User, reverse_delete_rule=1)
    
    title = db.StringField()

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )
    
    # 0 - just created
    # 1 - in progress
    # 2 - paused
    # 3 - finished

    @classmethod
    def async_aggreagte_lists(cls, owner_id):
        pipeline = [
            {"$lookup" : {
                "from" : "prospects",
                "let" : { "list_id": "$_id"},
                "pipeline" : [
                        {"$match": { "owner": owner_id } },
                        {"$group" : {
                            '_id':"$assign_to_list", 
                            'count' : {'$sum' : 1},
                            "owner": { "$first": "$owner"},
                            }
                        },
                        { "$match":
                            { "$expr":
                                { "$and":
                                    [
                                        { "$ne" :["$_id", None] },
                                        { "$eq": [ "$_id",  "$$list_id" ] },
                                    ]
                                }
                            }
                        },
                ],
                "as" : "grouped_prospects"
            }},
            {
                "$project" : {
                    "_id" : 1,
                    "title" : 1,
                    "grouped_prospects" : 1,
                    "total" : {
                        "$map" : {
                                "input" : "$grouped_prospects",
                                "as": "g",
                                "in" : { "$cond": {
                                            "if": {"$ne": ["$$g.count", None]},
                                            "then": "$$g.count",
                                            "else": 0
                                                }
                                        }
                        }
                    }
                }
            }
        ]


        lists = list(ProspectsList.objects(owner=owner_id).aggregate(*pipeline))

        sz = bson_dumps(lists)
        return sz

    @classmethod
    def get_lists_with_prospects_without_campaigns(cls, owner_id):
        lists_refs = Prospects.objects(owner=owner_id, assign_to=None).distinct('assign_to_list')
        if not lists_refs:
            return []
        
        
        list_ids = [l.id for l in lists_refs]
        lists = cls.objects(owner=owner_id, id__in=list_ids)

        results = lists.to_json()
        return results

    @classmethod
    def async_lists(cls, owner_id, page=1):
        db_query = cls.objects(owner=owner_id). \
                    only('id', 'title')
        
        total = db_query.count()
        prospects_list = db_query.order_by('-created')

        results = prospects_list.to_json()
        return (total, results)

    @classmethod
    def get_lists(cls, owner, title=None, id=None):
        if title:
            return cls.objects(owner=owner, title=title).first()
        elif id is not None:
            return cls.objects(owner=owner, id=id).first()
        else:
            return cls.objects(owner=owner)

    @classmethod
    def create_list(cls, owner_id, title):
        new_list = cls()
        
        new_list.owner = owner_id
        new_list.title = title

        new_list._commit(_reload=True)
        return new_list
    
    def serialize(self):
        return 0

    def update_data(self, title=None, _reload=False):
        if title:
            self.title = title
            self._commit(_reload=_reload)

    def safe_delete(self):
        has_prospects = Prospects.objects(assign_to_list=self.id).count()
        if has_prospects > 0:
            raise Exception("LIST DELETE ERROR: Remove prospects from the list, before delete")

        return self.delete()

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()


class Prospects(db.Document):
    RESTRICTED_SET_FIELDS = [
        'owner',
        'id',
        '_id',
        'status',
        'created',
        'assign_to'
    ]

    MEDIUM = ['email', 'linkedin', 'Email', 'Linkedin']
    
    @classmethod
    def get_create_fields(cls):
        return cls._fields.keys()

    owner = db.ReferenceField(User, reverse_delete_rule=1)
    
    team = db.ListField(db.ReferenceField(Team, reverse_delete_rule=1))
    
    data = db.DictField()

    assign_to = db.ReferenceField(Campaign, reverse_delete_rule=1)
    
    # 0 - just created
    # 1 - in progress
    # 2 - paused
    # 3 - finished
    status = db.IntField(default=0)
    
    # DO_NOTHING (0) - don’t do anything (default).
    # NULLIFY (1) - Updates the reference to null.
    # CASCADE (2) - Deletes the documents associated with the reference.
    # DENY (3) - Prevent the deletion of the reference object.
    # PULL (4) - Pull the reference from a ListField of references
    assign_to_list = db.ReferenceField('ProspectsList')
    tags = db.ListField(db.StringField())

    created = db.DateTimeField( default=pytz.utc.localize(datetime.utcnow()) )

    def serialize(self):
        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "assign_to",
                "foreignField" : "_id",
                "as" : "assign_to"
            }},
            { "$unwind" : { "path" : "$assign_to", "preserveNullAndEmptyArrays": True }},

            {"$lookup" : {
                "from" : "prospects_list",
                "localField" : "assign_to_list",
                "foreignField" : "_id",
                "as" : "assign_to_list"
            }},
            { "$unwind" : { "path" : "$assign_to_list", "preserveNullAndEmptyArrays": True }}
        ]

        prospect = list(Prospects.objects(id=self.id).aggregate(*pipeline))

        if len(prospect) > 0:
            prospect = prospect[0]

        sz = bson_dumps(prospect)

        return sz

    def _async_set_field(self, field_name, val):
        setattr(self, field_name, val)

    def _chek_for_duplicates(self, owner_id, data):
        if not data:
            return False
        
        query = {
            'owner' : owner_id,
            '_id' : { '$ne' : self.id }
        }

        check_duplicate = False
        or_array = []

        email = data.get('email','')
        if email:
            or_array.append(
                {
                    'data.email' : email
                }
            )
            check_duplicate = True

        linkedin = data.get('linkedin','')
        if linkedin:
            or_array.append(
                {
                    'data.linkedin' : linkedin
                }
            )
            check_duplicate = True

        if check_duplicate:
            query['$or'] = or_array
            duplicates = Prospects.objects(__raw__=query)
            if duplicates:
                error = "Duplicate found ERROR: email:{0} or linkedin:{1} exists".format(email, linkedin)
                raise Exception(error)


    def _validate_prospect_data(self, owner_id, prospect_data):
        
        assign_to_list = prospect_data.assign_to_list()
        if assign_to_list:
            exist = ProspectsList.objects(owner=owner_id, id=assign_to_list).first()
            if not exist:
                raise Exception("Prospect List doesn't exist")
        
        #check for email duplicate
        data = prospect_data.data()
        self._chek_for_duplicates(owner_id=owner_id, data=data)

        return True
    
    def add_tag(self, title):
        if title not in self.tags:
            self.tags.append(title)
        
        self._commit()

    def add_tags(self, tags):
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)

        self._commit()

    def has_all_data(self, need_data):
        tags = []
        if not need_data:
            return tags
        
        linkedin = self.data.get('linkedin', '')
        email = self.data.get('email', '')

        for d in need_data:
            if d == 'email':
                if not email:
                    tags.append('no_email')
            
            if d == 'linkedin':
                if not linkedin:
                    tags.append('no_linkedin')

        return tags

    @classmethod
    def export_all(cls, owner_id):
        db_query = cls.objects(owner=owner_id)
        if not db_query:
            return None

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "assign_to",
                "foreignField" : "_id",
                "as" : "assign_to"
            }},
            { "$unwind" : { "path" : "$assign_to", "preserveNullAndEmptyArrays": True }},
            {"$lookup" : {
                "from" : "prospects_list",
                "localField" : "assign_to_list",
                "foreignField" : "_id",
                "as" : "assign_to_list"
            }},
            { "$unwind" : { "path" : "$assign_to_list", "preserveNullAndEmptyArrays": True }},
            { "$project" : { 
                "data" : 1,
                "assign_to" : 1,
                "status" : 1,
                "tags" : 1,
                "assign_to_list" : 1
            }}
        ]

        prospects = list(db_query.order_by('-created').aggregate(*pipeline))
        
        csv.register_dialect("custom", delimiter=";")

        si = io.StringIO()
        cw = csv.writer(si, dialect="custom")

        csv_headers = list(CSV_EXPORT_HEADERS.keys())
        cw.writerow(csv_headers)

        for p in prospects:
            next_row = []
            for header, value in CSV_EXPORT_HEADERS.items():
                val = p.get(value, '-')
                if '#' in value:
                    prop, field = value.split('#')
                    if prop and field:
                        data = p.get(prop, '')
                        if data:
                            val = data.get(field, '')
                next_row.append(val)
            cw.writerow(next_row)

        return si.getvalue()

    @classmethod
    def enrich_prospect(cls, owner_id, prospect_id, prospect_data):
        if not prospect_data:
            raise Exception("Can't enrich from empty prospect_data")
        
        if not owner_id:
            raise Exception("Can't enrich for empty owner_id")

        prospect = cls.objects(id=prospect_id, owner=owner_id).first()
        if not prospect:
            message = "No such prospect_id={0} owner_id={1}".format(prospect_id, owner_id)
            raise Exception(message)

        prospect.data['enriched_data'] = prospect_data

        prospect_details = prospect_data.get('prospect_details', None)
        if prospect_details:
            first_name = prospect_details.get('first_name', '')
            if first_name:
                prospect.data['first_name'] = first_name
             
            last_name = prospect_details.get('last_name', '')
            if last_name:
                prospect.data['last_name'] = last_name
            
            email = prospect_details.get('email', '')
            if email:
                prospect.data['email'] = email
        
        prospect._commit()
        return True


    @classmethod
    def get_from_list(cls, owner_id, list_id):
        return cls.objects(owner=owner_id, assign_to_list=list_id)

    @classmethod
    def async_create(cls, owner_id, prospect_data, create_fields, restricted_fields=None):
        if not restricted_fields:
            restricted_fields = cls.RESTRICTED_SET_FIELDS

        new_prospect = cls()
        new_prospect.owner = owner_id

        new_prospect._validate_prospect_data(owner_id=owner_id, prospect_data=prospect_data)

        for field in create_fields:
            if field in restricted_fields:
                continue
    
            val = prospect_data.get_field(field)
            if val:
                new_prospect._async_set_field(field_name=field, val=val)

        new_prospect._commit(_reload=True)
        return new_prospect



    #we use this for test only
    @classmethod
    def create_prospect(cls, owner_id, data={}, list_id=None, campaign_id=None, commit=True):
        new_prospect = cls()

        new_prospect.owner = owner_id

        if data:
            new_prospect.data = data

        if list_id:
            new_prospect.assign_to_list = list_id

        obj_fields = cls.get_create_fields()

        prod_data = {}
        for key, val in data.items():
            if not data[key]:
                continue

            if key in obj_fields:
                setattr(new_prospect, key, data[key])
            else:
                prod_data[key] = val
        
        #DEPRECATED FIELDS USED BY TEST - need to remove
        if campaign_id:
            new_prospect.assign_to = campaign_id

        if commit:
            new_prospect._commit()

        return new_prospect

    @classmethod
    def filter_no_campaign(cls, owner_id, prospects_ids):
        return Prospects.objects(owner=owner_id, id__in=prospects_ids, assign_to=None)

    @classmethod
    def _unassign_campaign(cls, owner_id, prospects_ids):
        if not prospects_ids:
            return 0

        return Prospects.objects(owner=owner_id, 
                                id__in=prospects_ids).update(assign_to=None, status=NEW)

    @classmethod
    def _assign_campaign_on_create(cls, owner_id, campaign_id, prospects_ids):
        if not prospects_ids or not campaign_id:
            return 0

        return Prospects.objects(owner=owner_id,
                                assign_to=None, 
                                id__in=prospects_ids).update(status=NEW, assign_to=campaign_id)


    @classmethod
    def _assign_campaign(cls, owner_id, prospects_ids, campaign_id):
        if not prospects_ids or not campaign_id:
            return 0

        return Prospects.objects(owner=owner_id, 
                                id__in=prospects_ids).update(assign_to=campaign_id)


    #Only prospects that are not assigned to any campaign will be remove
    @classmethod
    def delete_prospects(cls, owner_id, prospects_ids):
        if not prospects_ids:
            return 0

        return Prospects.objects(owner=owner_id, id__in=prospects_ids, assign_to=None).delete()
    
    @classmethod
    def duplicates(cls, owner_id):
        def split_helper(obj, duplicates_dict):
            if not obj:
                return

            element = obj.get('_id', '')
            if not element:
                return 
            
            email = element.get('email','')
            if email:
                duplicates_dict['email'].append(email)

            linkedin = element.get('linkedin', '')
            if linkedin:
                duplicates_dict['linkedin'].append(linkedin)
        
            prospect_id = obj.get('prospect_id', '')
            if prospect_id:
                duplicates_dict['ids'].append(prospect_id)

        pipeline = [
            {"$group" : {
                "_id" : {
                    'email' : '$data.email',
                    'linkedin' : '$data.linkedin' 
                },
                "prospect_id" : {"$first" : { "$toString" : "$_id" }}
            }}        
        ]

        prospects = list(Prospects.objects(owner=owner_id).aggregate(*pipeline))

        duplicates = {
            'email' : [],
            'linkedin' : [],
            'ids' : []
        }

        q = [split_helper(p, duplicates) for p in prospects]

        return duplicates

    @classmethod
    def update_duplicates(cls, owner_id, new_data, values=[], list_id=None):
        duplicates = Prospects.objects(Q(owner=owner_id) & (Q(data__email__in=values) | Q(data__linkedin__in=values)))
        if not duplicates:
            return

        for prospect in duplicates:
            email = prospect.data.get('email', '')
            linkedin = prospect.data.get('linkedin', '')
            for data in new_data:
                if (data.get('email', '') and email == data['email']) or (data.get('linkedin', '') and linkedin == data['linkedin']):
                    prospect.data = data
                    if list_id:
                        prospect.assign_to_list = list_id
                    prospect._commit()
                    del data
                    break
    
    @classmethod
    def upload_from_list(cls, owner_id, prospects_arr, list_id, update_existing=0):
        if not prospects_arr:
            return False

        emails = []
        linkedins = []

        create_prospects = {}
        for prospect in prospects_arr:
            email = prospect.get('email', '')
            linkedin = prospect.get('linkedin', '')
            if not email and not linkedin:
                continue
            
            next_prospect = cls.create_prospect(owner_id=owner_id,
                                                data=prospect, 
                                                list_id=list_id, 
                                                commit=False)

            if linkedin:
                create_prospects[linkedin] = next_prospect
                linkedins.append(linkedin)
                continue

            if email:
                create_prospects[email] = next_prospect
                emails.append(email)
                continue
                    
        # we have found duplicates
        if emails or linkedins:
            duplicates = Prospects.objects(Q(owner=owner_id) & (Q(data__email__in=emails) | Q(data__linkedin__in=linkedins)))
            if duplicates and len(duplicates):
                for d in duplicates:
                    try:
                        linkedin = d.get_linkedin()
                        email = d.get_email()

                        key = linkedin
                        prospect = create_prospects.get(linkedin, None)
                        if not prospect:
                            key = email
                            prospect = create_prospects.get(email, None)
                        
                        if prospect:
                            if update_existing:
                                new_data = prospect.data
                                d.update_data_partly(new_data=new_data, list_id=list_id)
                            del create_prospects[key]

                    except:
                        pass

            arr = list(create_prospects.values())
            if arr:
                cls.objects.insert(arr, load_bulk=False)
        
        return True

    @classmethod
    def upload(cls, owner_id, csv_with_header, map_to, list_id, update_existing=0):

        prospects_list = []
        need_update = []
        duplicate_values = []

        #dict with
        # 'email' : [] (All current emails)
        # 'linkedin' : [] (All current linkedins)
        # 'ids' : [] (All ids)
        duplicates = cls.duplicates(owner_id=owner_id)

        i = 0
        for row in csv_with_header:
            i = i + 1

            #pass header
            if i == 1:
                continue

            data = {}
            found_duplicate = False
            just_pass = False
            for m_t in map_to.keys():
                row_data = row[m_t]
                field_name = map_to[m_t]

                data[field_name] = row_data
                if field_name in cls.MEDIUM:
                    #check if it exists in database
                    if row_data in duplicates['email'] or row_data in duplicates['linkedin']:
                        #check if we already seen this one (there could be duplicates in the CSV too)
                        if row_data not in duplicate_values:
                            found_duplicate = True
                            duplicate_values.append(row_data)
                        else:
                            just_pass = True
                            break

            if just_pass:
                continue
            elif found_duplicate:
                need_update.append(data)
            else:
                next_prospect = cls.create_prospect(owner_id=owner_id,
                                                    data=data, 
                                                    list_id=list_id, 
                                                    commit=False)
                prospects_list.append(next_prospect)

        # create the new prospects first
        ids = []
        if prospects_list:
            ids = cls.objects.insert(prospects_list, load_bulk=False)
        
        #then update existing ones
        if update_existing:
            cls.update_duplicates(owner_id=owner_id, new_data=need_update, values=duplicate_values, list_id=list_id)

        return len(ids)

    @classmethod
    def count_prospects_in_a_list(cls, list_id):
        return Prospects.objects(assign_to_list=list_id).count()

    @classmethod
    def add_to_list(cls, owner_id, prospects_ids, list_id):
        if not prospects_ids or not list_id:
            return 0
        
        list_exist = ProspectsList.objects(id=list_id).first()
        if not list_exist:
            raise Exception("List doesn't exist")
        
        res = Prospects.objects(owner=owner_id, id__in=prospects_ids).update(assign_to_list=list_id)

        return res
    
    @classmethod
    def remove_from_list(cls, owner_id, prospects_ids):
        if not owner_id or not prospects_ids:
            return 0
        
        res = Prospects.objects(owner=owner_id, id__in=prospects_ids).update(assign_to_list=None)

        return res


    @classmethod
    def async_prospects_list(cls, owner, list_filter, page, per_page=config.PROSPECTS_PER_PAGE):
        if page <= 1:
            page = 1

        filter_fields = ['assign_to', 'assign_to_list', 'column', 'contains']     

        #remove denied values
        list_filter.pop('owner', '')
        list_filter.pop('_id', '')

        #construct list_filter
        #list_filter = {'field_name' : {'operator' : 'value'}}
        query = {
            'owner' : owner
        }
        without_prefix = cls.get_create_fields()
        q = construct_prospect_filter(filter_data=list_filter,
                                        without_prefix = without_prefix,
                                        filter_fields=filter_fields)
        if q:
            query.update(q)

        db_query = cls.objects(**query)
        
        total = db_query.count()

        #we use it for join and showing objects as it is
        pipeline = [
            {"$lookup" : {
                "from" : "campaign",
                "localField" : "assign_to",
                "foreignField" : "_id",
                "as" : "assign_to"
            }},
            { "$unwind" : { "path" : "$assign_to", "preserveNullAndEmptyArrays": True }},
            {"$lookup" : {
                "from" : "prospects_list",
                "localField" : "assign_to_list",
                "foreignField" : "_id",
                "as" : "assign_to_list"
            }},
            { "$unwind" : { "path" : "$assign_to_list", "preserveNullAndEmptyArrays": True }},
            { "$project" : { 
                "team" : 1,
                "data" : 1,
                "assign_to" : 1,
                "status" : 1,
                "tags" : 1,
                "assign_to_list" : 1
            }}
        ]

        prospects = db_query.skip(per_page * (page-1)).limit(per_page).order_by('-created').aggregate(*pipeline)

        results = bson_dumps(prospects)

        return (total, results)

    @classmethod
    def check_new_parsed_prospects(cls, campaign_id, list_id):
        cls.objects(assign_to_list=list_id, assign_to=None).update(assign_to=campaign_id, status=NEW)

    @classmethod
    def get_prospects(cls, status=None, campaign_id=None):
        if status is None and campaign_id is None:
            raise Exception("Status and campaign_id can't be None")
        
        if status is not None:
            return cls.objects(Q(status=status) & Q(assign_to=campaign_id)).order_by('-created')
        else:
            return cls.objects(assign_to=campaign_id)


    @classmethod
    def update_prospects(cls, ids, status):
        return cls.objects(id__in=ids).update(status=status)

    def get_data(self):
        return self.data

    def get_email(self):
        return self.data.get('email', '')
    
    def get_linkedin(self):
        return self.data.get('linkedin', '')

    def update_data_partly(self, new_data, list_id=None, _reload=False):
        if not new_data:
            return 

        for k, v in new_data.items():
            self.data[k] = v

        if list_id:
            self.assign_to_list = list_id

        self._commit(_reload=_reload)

    def update_data(self, data, _reload=False):
        self._chek_for_duplicates(owner_id=self.owner.id, data=data)

        self.data = data
        self._commit(_reload=_reload)

    def update_status(self, status):
        self.status = status

        self._commit()

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()


class MediumSettings(db.Document):
    # which medium
    medium = db.StringField()

    per_day = db.IntField()
    per_hour = db.IntField()

    interval = db.IntField()

class Templates(db.Document):
    label = db.StringField()
    data = db.DictField()
    status = db.IntField()

class MergeTags(db.Document):
    tag_name = db.StringField()
    tag_value = db.DictField()


#Register delete rules for '' ReferenceFields as described here: https://github.com/MongoEngine/mongoengine/issues/1707

ProspectsList.register_delete_rule(Prospects, "assign_to_list", 1)
