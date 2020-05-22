import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel
import random
import string
from flask import url_for
import json
from pprint import pprint
from bson.objectid import ObjectId
from datetime import datetime
import pytz
from o24.globals import *

from o24.production_tests.test_data import *
from o24.backend.utils.decors import get_token
import string
import random

TEST_USER_EMAIL = '1@email.com'

def random_num(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def post_with_token(user, client, url, data):
    token = get_token(user)
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }
    print("Sending request to url:{0}".format(url))
    pprint(data)
    
    r = None
    if data:        
        r = client.post(url, data=data, content_type='multipart/form-data', headers=headers, follow_redirects=False)
    else:
        r = client.post(url, content_type='multipart/form-data', headers=headers, follow_redirects=False)

    return r


class ProdTestScenaries(unittest.TestCase):
    def setUp(self):
        pass

    def test_0_check_linkedin_campaigns_handlers(self):
        user = User.objects(email=TEST_USER_EMAIL).first()
        linkedin_credentials = Credentials.get_credentials(user_id=user.id, medium='linkedin')

        client = app.test_client()    
        with app.test_request_context():
            #CREATE parse LINKEDIN campaign
            LINKEDIN_PARSE_CAMPAIGN_ID = self._create_linkedin_parsing_campaign(user=user, 
                                                                credentials=linkedin_credentials, 
                                                                client=client)

            #EDIT parse LINKEDIN campaign
            self._edit_linkedin_campaign(user=user, 
                                        client=client,
                                        campaign_id=LINKEDIN_PARSE_CAMPAIGN_ID)
        
            #CREATE enrichment LINKEDIN campaign
            LINKEDIN_ENRICH_CAMPAIGN_ID = self._create_linkedin_enrichment_campaign(user=user, 
                                                                client=client)

            #LIST LINKEDIN campaigns
            LIST_LINKEDIN_CAMPAIGNS = self._list_linkedin_campaigns(user=user, client=client)   

            #START Linkedin Campaign Parse
            
            #get campaign with parse type
            PARSE_LINKEDIN_CAMPAIGN = None
            for c in LIST_LINKEDIN_CAMPAIGNS:
                if c['campaign_type'] == LINKEDIN_PARSING_CAMPAIGN_TYPE:
                    PARSE_LINKEDIN_CAMPAIGN = c
                    break
            
            if not PARSE_LINKEDIN_CAMPAIGN:
                self.assertTrue(False, "Can't find LINKEDIN_PARSING_CAMPAIGN_TYPE in LIST_LINKEDIN_CAMPAIGNS list")

            #start
            self._start_linkedin_campaign(user=user, client=client, campaign_id=PARSE_LINKEDIN_CAMPAIGN['_id']['$oid'])

            #PAUSE Linkedin Campaign Parse
            self._pause_linkedin_campaign(user=user, client=client, campaign_id=PARSE_LINKEDIN_CAMPAIGN['_id']['$oid'])


            #DELETE Linkedin Campaign Parse
            self._delete_linkedin_campaign(user=user, client=client, campaign_id=PARSE_LINKEDIN_CAMPAIGN['_id']['$oid'])

            #START Linkedin Campaign Enrichment
            #get campaign with parse type
            ENRICHMENT_LINKEDIN_CAMPAIGN = None
            for c in LIST_LINKEDIN_CAMPAIGNS:
                if c['campaign_type'] == LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE:
                    ENRICHMENT_LINKEDIN_CAMPAIGN = c
                    break
            
            if not ENRICHMENT_LINKEDIN_CAMPAIGN:
                self.assertTrue(False, "Can't find LINKEDIN_PARSING_CAMPAIGN_TYPE in LIST_LINKEDIN_CAMPAIGNS list")

            #start
            self._start_linkedin_campaign(user=user, client=client, campaign_id=ENRICHMENT_LINKEDIN_CAMPAIGN['_id']['$oid'])

            #PAUSE Linkedin Campaign Enrichment
            self._pause_linkedin_campaign(user=user, client=client, campaign_id=ENRICHMENT_LINKEDIN_CAMPAIGN['_id']['$oid'])

            #DELETE Linkedin Campaign Enrichment
            self._delete_linkedin_campaign(user=user, client=client, campaign_id=ENRICHMENT_LINKEDIN_CAMPAIGN['_id']['$oid'])


    def test_1_check_campaigns_handlers(self):
        user = User.objects(email=TEST_USER_EMAIL).first()

        client = app.test_client()    
        with app.test_request_context():
 #LIST OUTREACH campaigns
            url = url_for('dashboard.list_campaigns')
            r = post_with_token(user=user, client=client, url=url, data=None)

            response_data = json.loads(r.data)
            pprint(response_data)
            code = response_data['code']
            msg = response_data['msg']
            error_message = "msg: {0}".format(msg)
            self.assertTrue(code == 1, error_message)

        #check that campaigns are GENERAL type ONLY
            campaigns = json.loads(response_data['campaigns'])
            for campaign in campaigns:
                if campaign['campaign_type'] != OUTREACH_CAMPAIGN_TYPE:
                    error = "ERROR list_campaigns response: MUST show only OUTREACH_CAMPAIGN_TYPE campaigns, but have LINKEDIN campaign.id={0} campaign.title={1}".format(campaign.id, campaign.title)
                    self.assertTrue(False, message)

    def test_2_check_admin_handlers(self):
        user = User.objects(email=TEST_USER_EMAIL).first()

        client = app.test_client()    
        with app.test_request_context():

            #CREATE GOOGLE APP SETTINGS
            SETTINGS_ID = self._admin_google_settings_create(user=user, client=client)

            #EDIT GOOGLE APP SETTINGS
            #EDIT parse LINKEDIN campaign
            self._admin_google_settings_edit(user=user, 
                                        client=client,
                                        settings_id=SETTINGS_ID)


    def _delete_linkedin_campaign(self, user, client, campaign_id):
        form_data = {
            '_campaign_id' : campaign_id,
        }

        url = url_for('dashboard.delete_linkedin_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        pprint(response_data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)
    
    #check deleted
        deleted = Campaign.objects(id=campaign_id).first()
        if deleted:
            error = "Campaign didn't deleted still in a database id={0}".format(deleted.id)
            self.assertTrue(False, error)
        
        return True


    def _pause_linkedin_campaign(self, user, client, campaign_id):
        form_data = {
            '_campaign_id' : campaign_id,
        }

        url = url_for('dashboard.pause_linkedin_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        pprint(response_data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

        paused = json.loads(response_data['paused'])
        error = "Wrong campaign paused  need id:{0}  has id:{1}".format(campaign_id, paused['_id']['$oid'])
        self.assertTrue(paused['_id']['$oid'] == campaign_id, error)

        error = "Campaign didn't paused status={0}".format(paused['status'])
        self.assertTrue(paused['status'] == PAUSED, error)

        return paused

    def _start_linkedin_campaign(self, user, client, campaign_id):
        form_data = {
            '_campaign_id' : campaign_id,
        }

        url = url_for('dashboard.start_linkedin_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        pprint(response_data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

        started = json.loads(response_data['started'])
        error = "Wrong campaign started  need id:{0}  has id:{1}".format(campaign_id, started['_id']['$oid'])
        self.assertTrue(started['_id']['$oid'] == campaign_id, error)

        error = "Campaign didn't started status={0}".format(started['status'])
        self.assertTrue(started['status'] == IN_PROGRESS, error)

        return started


    def _edit_linkedin_campaign(self, user, client, campaign_id, req_dict=None):
    #get first
        form_data = {
            '_campaign_id' : campaign_id
        }
        url = url_for('dashboard.get_linkedin_campaign_by_id')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

    #check campaign id
        get_campaign = json.loads(response_data['campaign'])
        pprint(get_campaign)
        modified_fields = json.loads(response_data['modified_fields'])
        self.assertTrue(modified_fields, "get_linkedin_campaign_by_id returned empty modified fields")

        
        message = "Get wrong campaign id {0}".format(get_campaign['_id']['$oid'])
        self.assertTrue(get_campaign['_id']['$oid'] == campaign_id, message)
        

    #then edit
        _req_dict = None
        if req_dict:
            _req_dict = req_dict
        else:
            _req_dict = CAMPAIGN_LINKEDIN_EDIT
            _req_dict['title'] = _req_dict['title'].format(random_num())
            _req_dict['data']['search_url'] = _req_dict['data']['search_url'].format(random_num())
        
        json_create_data = json.dumps(_req_dict)
        form_data = {
            '_campaign_id' : get_campaign['_id']['$oid'],
            '_add_campaign' : json_create_data,
            '_modified_fields' : json.dumps(modified_fields)
        }
        
        url = url_for('dashboard.edit_linkedin_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

        updated_campaign = json.loads(response_data['updated'])
        pprint(updated_campaign)
        self.assertTrue(updated_campaign['_id']['$oid'] == get_campaign['_id']['$oid'], "Updated campaign ID not equal get campaign ID")
        #compare fields
        for k,v in _req_dict.items():
            if k == 'data':
                u_data = updated_campaign['data']
                for k1, v1 in v.items():
                    u_v1 = u_data[k1]
                    error = "Error update DATA need:{0}  has:{1}".format(v1, u_v1)
                    self.assertTrue(v1 == u_v1, error)
            else:
                if k == 'from_hour' or k == 'to_hour':
                    v = int(v.split(':')[0])

                u_v = updated_campaign[k]
                error = "Error update key:{0} need:{1}  has:{2}".format(k, v, u_v)
                self.assertTrue(v == u_v, error)
        
        return updated_campaign
    
    def _list_linkedin_campaigns(self, user, client):
        url = url_for('dashboard.list_linkedin_campaigns')
        r = post_with_token(user=user, client=client, url=url, data=None)

        response_data = json.loads(r.data)
        pprint(response_data)

        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

    #check that campaigns are not GENERAL type
        LIST_LINKEDIN_CAMPAIGNS = json.loads(response_data['campaigns'])
        for campaign in LIST_LINKEDIN_CAMPAIGNS:
            if campaign['campaign_type'] == OUTREACH_CAMPAIGN_TYPE:
                error = "ERROR list_linkedin_campaigns response: MUST show only Linkedin campaigns, but have OUTREACH campaign.id={0} campaign.title={1}".format(campaign.id, campaign.title)
                self.assertTrue(False, message)

        return LIST_LINKEDIN_CAMPAIGNS

    def _data_linkedin_campaign(self, user, client):
    #get data first        
        url = url_for('dashboard.data_linkedin_campaign')
        r = post_with_token(user=user, client=client, url=url, data=None)

        response_data = json.loads(r.data)
        pprint(response_data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

        return response_data


    def _create_linkedin_enrichment_campaign(self, user, client, req_dict=None):
        _req_dict = None

        response_data = self._data_linkedin_campaign(user=user, client=client)

        credentials = []
        lists = []
        try:
            credentials = json.loads(response_data['credentials'])
        except Exception as e:
            error = "BROKEN TEST DATA: There is no credentials for this user, excepton: {0}".format(str(e))
            self.assertTrue(False, error)

        try:
            lists = json.loads(response_data['lists'])
        except Exception as e:
            error = "BROKEN TEST DATA: There is no prospects lists with assign_to=None for this user, excepton: {0}".format(str(e))
            self.assertTrue(False, error)

        linkedin_credentials = None
        for cr in credentials:
            if cr.get('medium', '') == 'linkedin':
                linkedin_credentials =cr
                break

        if linkedin_credentials is None:
            self.assertTrue(False, "BROKEN TEST DATA: There is no linkedin credentials for this user")

        list_selected = lists[0]
    
    #now create
        if req_dict:
            _req_dict = req_dict
        else:
            _req_dict = CAMPAIGN_LINKEDIN_ENRICHMENT_CREATE
            _req_dict['title'] = _req_dict['title'].format(random_num())
            _req_dict['list_selected'] = list_selected
            _req_dict['credentials'].append(linkedin_credentials)

        json_create_data = json.dumps(_req_dict)
        form_data = {
            '_add_campaign' : json_create_data,
        }
        
        url = url_for('dashboard.create_linkedin_enrichment_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

    #check campaign type
        added = json.loads(response_data['added'])
        pprint(added)
        message = "Created wrong campaigntype {0}".format(added['campaign_type'])
        self.assertTrue(added['campaign_type'] == LINKEDIN_ENRICHMENT_CAMPAIGN_TYPE, message)
        
    #check funnel
        message = "Created wrong funnel type {0}".format(added['funnel']['funnel_type'])
        self.assertTrue(added['funnel']['funnel_type'] == LINKEDIN_ENRICHMENT_FUNNEL_TYPE, message)

        return added['_id']['$oid']



    def _create_linkedin_parsing_campaign(self, user, credentials, client, req_dict=None):
        _req_dict = None

        if req_dict:
            _req_dict = req_dict
        else:
            _req_dict = CAMPAIGN_LINKEDIN_PARSING_CREATE
            _req_dict['title'] = _req_dict['title'].format(random_num())
            _req_dict['list_title'] = _req_dict['list_title'].format(random_num())
            
            credentials_dict = json.loads(credentials.to_json())
            _req_dict['credentials'].append(credentials_dict)


        json_create_data = json.dumps(_req_dict)
        form_data = {
            '_add_campaign' : json_create_data
        }
        
        url = url_for('dashboard.create_linkedin_parsing_campaign')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

    #check campaign type
        added = json.loads(response_data['added'])
        pprint(added)

        message = "Created wrong campaigntype {0}".format(added['campaign_type'])
        self.assertTrue(added['campaign_type'] == LINKEDIN_PARSING_CAMPAIGN_TYPE, message)
        
    #check funnel
        message = "Created wrong funnel type {0}".format(added['funnel']['funnel_type'])
        self.assertTrue(added['funnel']['funnel_type'] == LINKEDIN_PARSING_FUNNEL_TYPE, message)

        return added['_id']['$oid']

    def _admin_google_settings_create(self, user, client, req_dict=None):
        _req_dict = None

        if req_dict:
            _req_dict = req_dict
        else:
            _req_dict = ADMIN_GOOGLE_SETTINGS_CREATE
            _req_dict['title'] = _req_dict['title'].format(random_num())

        json_create_data = json.dumps(_req_dict)
        form_data = {
            '_data' : json_create_data
        }
        
        url = url_for('dashboard.admin_google_settings_create')
        r = post_with_token(user=user, client=client, url=url, data=form_data)

        response_data = json.loads(r.data)
        code = response_data['code']
        msg = response_data['msg']
        error_message = "msg: {0}".format(msg)
        self.assertTrue(code == 1, error_message)

    #check campaign type
        settings = json.loads(response_data['settings'])
        pprint(settings)

        return settings['_id']['$oid']


def setUpModule():
    print("*** setUpModule:{0}".format(__name__))

    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

    #drop_database()
    #create_models()

if __name__ == '__main__':
    unittest.main()
        

