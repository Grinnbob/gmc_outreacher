import o24.backend.dashboard.models as models 
from o24.globals import *
from o24.backend import db
from mongoengine.queryset.visitor import Q
from datetime import datetime
import pytz
import o24.config as config
import string
import random
import re

week_day_map = {
    0 : 'Mon',
    1 : 'Tue',
    2 : 'Wed',
    3 : 'Thu',
    4 : 'Fri',
    5 : 'Sat',
    6 : 'Sun'
}

month_map = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'Jun',
    7 : 'Jul',
    8 : 'Aug',
    9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
}

class BouncedMessages(db.Document):
    owner = db.ReferenceField('User')
    email = db.StringField()
    error = db.StringField()
    
    google_msg_id = db.StringField()
    google_thread_id = db.StringField()

    raw = db.StringField()
    created = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))

    @classmethod
    def _extract_id(cls, message):
        msg_id = '' 
        thread_id = ''
        if not message:
            return msg_id, thread_id
        
        msg_id = message.get('id', '')
        thread_id = message.get('threadId', '')

        return msg_id, thread_id

    @classmethod
    def _extract_error(cls, message):
        email = ''
        error = ''
        if not message:
            return email, error

        snippet = message.get('snippet', '')
        if snippet:
            error = str(snippet)
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", snippet)
            if len(emails) > 0:
                email = emails[0]

        return email, error

    @classmethod
    def has_messages(cls, owner_id, msg_ids):
        return cls.objects(owner=owner_id,
                            google_msg_id__in=msg_ids).distinct('google_msg_id')

    @classmethod
    def parse_messages(cls, owner_id, messages, search_email=None):
        if not messages:
            return False
        
        if not owner_id:
            raise Exception("parse_messages ERROR: owner_id can't be null = {0}".format(owner_id))
        
        found = False
        now = pytz.utc.localize(datetime.utcnow())

        for m in messages:
            email, error = cls._extract_error(message=m)
            if search_email and email == search_email:
                found = True

            msg_id, thread_id = cls._extract_id(message=m)
            new_bounced = cls(owner=owner_id,
                                raw=str(m),
                                created=now,
                                email=email,
                                error=error,
                                google_msg_id=msg_id,
                                google_thread_id=thread_id)
            new_bounced._commit()

        return found

    @classmethod
    def check_bounced(cls, owner_id, email, after):
        return cls.objects(owner=owner_id, 
                            email=email,
                            created__gte=after).first()

    def _commit(self):
        self.save()

class MailBox(db.Document):
    owner = db.ReferenceField('User')
    prospect_id = db.ReferenceField('Prospects')
    campaign_id = db.ReferenceField('Campaign')

    #it's incremented inside (prospect_id, campaign_id)
    # we setup -1 for draft
    sequence = db.IntField(default=0)

    email_data = db.DictField()

    sender_meta = db.DictField()

    # 1 - Intro
    # 2 - Followup
    message_type = db.IntField(default=0)

    # we don't use it now BUT
    # if we will need to create complex email sequence (with several intro's and followups) then
    # we will use this field to store task meta that this email belongs to 
    task_meta = db.DictField()

    created = db.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))

    @classmethod
    def sequence_start_date(cls, prospect_id, campaign_id, posix_time=True, last_one=False):
        _filter = 'created'
        if last_one:
            _filter = '-created'

        first_message = cls.objects(prospect_id=prospect_id, campaign_id=campaign_id).order_by(_filter).first()
        if not first_message:
            now = pytz.utc.localize(datetime.utcnow())
            if posix_time:
                return int(now.timestamp()) - 30
            else:
                return now
        
        created = first_message.created
        if posix_time:
            return int(created.timestamp()) - 30
        else:
            return created

    @classmethod
    def create_draft(cls, prospect_id, campaign_id):
        campaign = models.Campaign.objects(id=campaign_id).first()
        if not campaign:
            raise Exception("create_draft ERROR: There is no campaign_id={0}".format(campaign_id))

        new_message = cls()
        new_message.owner = campaign.owner.id

        new_message.sequence = -1
        new_message.prospect_id = prospect_id
        new_message.campaign_id = campaign_id

        new_message._commit(_reload=True)
        return new_message

    def get_owner_id(self):
        return self.owner.id    

    #need to redone
    def add_message(self, data, task_meta={}, message_type=1):

        has_parent = MailBox.get_parent(prospect_id=self.prospect_id,
                                            campaign_id=self.campaign_id)
        current_sequence = 0
        if has_parent:
            current_sequence = has_parent.sequence + 1

        self.sequence = current_sequence

        self.email_data = data.get('email_data')
        self.sender_meta = data.get('sender_meta')

        self.task_meta = task_meta
        self.message_type = message_type
    
        self._commit()
        return
    
    @classmethod
    def get_parent(cls, prospect_id, campaign_id):
        parent = cls.objects(sequence__gte=0, prospect_id=prospect_id, campaign_id=campaign_id).order_by('-sequence').first()
        if not parent:
            return None
        
        return parent

    @classmethod
    #msgId - Global goole msgId 
    def get_mailbox(cls, mailbox_id=None, msgId=None):
        if mailbox_id:
            return cls.obcjects(id=mailbox_id).first()
        
        if msgId:
            return cls.obcjects(email_data__msgId=msgId).first()

        return None

    def get_references(self):
        return self.email_data.get('references', '')
    
    def get_text(self):
        return self.email_data.get('text', '')

    def get_html(self):
        return self.email_data.get('html', '')

    def get_msgId(self):
        return self.email_data.get('msgId', '')

    def get_trail(self):
        return self.email_data.get('trail', '')

    def get_wrote_on_data(self):
        data_dict = {
            'sender' : '',
            'week_day' : '',
            'date' : '',
            'month' : '',
            'year' : ''
        }

        data_dict['sender'] = self.email_data.get('sender', '')

        date = self.created

        data_dict['week_day'] = week_day_map[date.weekday()]
        data_dict['date'] = date.day
        data_dict['month'] = month_map[date.month]
        data_dict['year'] = date.year

        return data_dict

    def get_thread_id(self):
        thread_id = ''

        api_res = self.email_data.get('api_res', '')
        if api_res:
            thread_id = api_res.get('threadId','')

        return thread_id

    def get_api_msg_id(self):
        msg_id = ''
        
        api_res = self.email_data.get('api_res', '')
        if api_res:
            msg_id = api_res.get('id','')

        return msg_id

    def set_msgId(self, msgId):
        self.email_data['msgId'] = msgId
        self._commit()

        return True

    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()


class TrackingDomains(db.Document):
    #config.DEFAULT_SUBDOMAIN_PREFIX

    owner = db.ReferenceField('User')

    domain = db.StringField(required=True)
    tracking_domain = db.StringField(required=True)
    
    used_by_emails = db.DictField()

    status = db.IntField(default=0) 

    NEW = 0 # just created
    VERIFIED = 1 #Verified(1) - DNS checked
    ACTIVE = 2 #Active(2) - certificate activated
    

    def domain_verified(self):
        self.status = self.VERIFIED
        self._commit()
    
    def domain_activated(self):
        self.status = self.ACTIVE
        self._commit()
    
    @classmethod
    def _domain_from_email(cls, email):
        splitted = email.split('@')
        if len(splitted) < 2:
            raise Exception("Wrong email format:{0}".format(email))

        domain = splitted[1]
        domain = domain.strip()

        return domain

    @classmethod
    def _build_tracking_domain(cls, domain):
        if not domain:
            raise Exception("_build_tracking_domain ERROR: domain can't be empty:{0}".format(domain))
        
        tracking_domain = config.DEFAULT_SUBDOMAIN_PREFIX + domain
        return tracking_domain

    @classmethod
    def get_tracking_domain(cls, owner_id, email):
        domain = cls._domain_from_email(email=email)
        if not domain:
            raise Exception("get_tracking_domain ERROR: wrong email format:{0}".format(email))

        found = config.DEAFULT_TRACKING_DOMAIN

        exist = cls.objects(owner=owner_id, 
                            domain=domain, 
                            status=cls.ACTIVE).first()
        if exist:
            found = exist.tracking_domain
        
        if not found:
            raise Exception("get_tracking_domain ERROR: tracking_domain can't be empty:{0}".format(found))

        return found

    @classmethod
    def create_tracking_domain(cls, owner_id, email):
        if not owner_id:
            raise Exception("onwer_id can't be empty")
        
        domain = cls._domain_from_email(email=email)
        if not domain:
            raise Exception("Wrong domain format:{0}".format(email))

        exist = cls.objects(owner=owner_id, domain=domain).first()
        if exist:
            if email not in exist.used_by_emails.keys():
                exist.used_by_emails[email] = pytz.utc.localize(datetime.utcnow())
                exist._commit()
            return exist
        
        new_domain = cls()
        new_domain.status = cls.NEW
        new_domain.owner = owner_id

        new_domain.domain = domain
        new_domain.tracking_domain = cls._build_tracking_domain(domain)

        new_domain.used_by_emails[email] = pytz.utc.localize(datetime.utcnow())
        new_domain._commit()

        return new_domain

    def _commit(self, _reload=False):
        self.save()


#1 message = 1 uniqueue code
#format: via.outreacher24.com/<type>/<code>/<event>:
class TrackEvents(db.Document):
    owner = db.ReferenceField('User')
    
    prospect_id = db.ObjectIdField()
    campaign_id = db.ObjectIdField()

    code = db.StringField(required=True)
    mailbox_id = db.ReferenceField(MailBox)

    opened = db.IntField(default=0)
    clicked = db.IntField(default=0)
    
    @classmethod
    def track_event(cls, code, event):
        exist = cls.objects(code=code).first()
        if not exist:
            raise Exception("There is not TrackEvents registered for code:{0}".format(code))
        
        counter = 0
        if event == 'open':
            exist.opened = exist.opened + 1
            counter = exist.opened
        elif event == 'click':
            exist.clicked = exist.clicked + 1
            counter = exist.clicked
        else:
            raise Exception("track_event ERROR: Unknown event={0}".format(event))
        
        exist._commit()

        owner_id = exist.owner.id
        return owner_id, counter, exist.prospect_id, exist.campaign_id

    @classmethod
    def get_create_tracking_event(cls, owner_id, mailbox_id):
        exist = cls.objects(owner=owner_id, mailbox_id=mailbox_id).first()
        if not exist:
            exist = cls()
            
            mailbox = MailBox.objects(id=mailbox_id).first()
            if not mailbox:
                raise Exception("get_create_tracking_event ERROR: can't find mailbox for id={0}".format(mailbox_id))
                
            exist.prospect_id = mailbox.prospect_id.id
            exist.campaign_id = mailbox.campaign_id.id

            exist.owner = owner_id
            exist.mailbox_id = mailbox_id
            exist.code = cls._random_code()

            exist._commit(_reload=True)

        return exist

    @classmethod
    def get_tracking_link(cls, owner_id, mailbox_id, email, event='open'):
        tracking_domain = TrackingDomains.get_tracking_domain(owner_id=owner_id, 
                                                                email=email)
        if not tracking_domain:
            raise Exception("get_tracking_link ERROR: tracking_domain can't be empty")
        
        exist = cls.get_create_tracking_event(owner_id=owner_id, mailbox_id=mailbox_id)
        if not exist:
            raise Exception("Can't get tracking event for owner_id={0} mailbox_id={1}".format(owner_id, mailbox_id))

        code = exist.code
        if not code:
            raise Exception("code can't be empty={0}".format(code))
        
        link = None
        if event == 'open':
            link = cls._build_tracking_link(event=event,
                                            tracking_domain=tracking_domain,
                                            code=code)
        else:
            raise Exception("Unknown tracking event type={0}".format(event))

        
        return link

    @classmethod
    def _random_code(cls, code_length=None):
        if not code_length:
            code_length = config.DEFAULT_CODE_LENGTH

        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(code_length))


    @classmethod
    def _build_tracking_link(cls, event, tracking_domain, code=code):
        
        tracking_type = ''
        if event == 'open':
            tracking_type = 'ot'
        elif event == 'click':
            tracking_type = 'ct'
        else:
            raise Exception("Unknown tracking event type={0}".format(event))

        link = '{tracking_domain}/{tracking_type}/{code}/{event}'.format(tracking_domain=tracking_domain,
                                                                        tracking_type=tracking_type,
                                                                        code=code,
                                                                        event=event)

        return link


    def _commit(self, _reload=False):
        self.save()
        if _reload:
            self.reload()