# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Prospects, User, Campaign, ProspectsList, Credentials
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import o24.config as config
from o24.backend.utils.serialize import JSONEncoder
from o24.backend.utils.helpers import template_key_dict, to_json_deep_dereference
import json
import traceback

import o24.backend.models.shared as shared
from o24.backend.dashboard.serializers import JSCampaignData
import o24.backend.scheduler.scheduler as scheduler
from o24.backend.utils.decors import auth_required


COLUMNS = [
    {
        'label' : 'Title',
        'prop' : 'title'
    },
    {
        'label' : 'Status',
        'prop' : 'status'
    },
    {
        'label' : 'Leads',
        'prop' : 'cache',
        'field' : 'leads_total'
    },
    {
        'label' : 'Proceed',
        'prop' : 'cache',
        'field' : 'leads_proceed'
    },
    {
        'label' : 'Sequence',
        'prop' : 'funnel',
        'field' : 'title',   
    },
]

modified_fields_on_create = {
    'title' : True,
    'funnel' : True,
    'credentials' : True,
    'templates' : True,
    'time_table' : True,
    'lists' : True,
    'time_zone' : True,
    'custom_delays' : True
}

modified_fields_on_edit = {
    'title' : True,
    'templates' : True,
    'time_table' : True,
    'funnel' : False,
    'credentials' : False,
    'lists' : False,
    'from_hour' : True,
    'to_hour' : True,
    'from_minutes' : True,
    'to_minutes' : True,
    'sending_days' : True,
    'time_zone' : True,
    'custom_delays' : True
}

@bp_dashboard.route('/campaigns/data', methods=['POST'])
@auth_required
def data_campaigns():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'lists' : '',
        'credentials' : '',
        'funnels' : '',
        'modified_fields' : json.dumps(modified_fields_on_create),
        'columns' : json.dumps(COLUMNS)
    }

    try:        
        if request.method == 'POST':
            lists = ProspectsList.get_lists(owner=current_user.id)
            if lists:
                result['lists'] = lists.to_json()

            total, credentials = Credentials.async_credentials(owner=current_user.id, active_only=True)
            if credentials:
                result['credentials'] = credentials
            
            funnels = shared.Funnel.async_funnels(funnel_types=[0])
            if funnels:
                result['funnels'] = funnels

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result), 200


@bp_dashboard.route('/campaigns/list', methods=['POST'])
@auth_required
def list_campaigns():
    current_user = g.user

    per_page = config.CAMPAIGNS_PER_PAGE
    page = 1

    pagination = {
            'perPage' : per_page,
            'currentPage' : page,
            'total' : 0
    }

    result = {
        'code' : -1,
        'msg' : '',
        'campaigns' : '',
        'modified_fields' : json.dumps(modified_fields_on_create),
        'pagination' : json.dumps(pagination),
        'columns' : json.dumps(COLUMNS)
    }

    try:
        if request.method == 'POST':
            page = int(request.form.get('_page',1))

            total, campaigns = Campaign.async_campaigns_list(owner=current_user.id,
                                                page=page)    
            if campaigns:
                result['campaigns'] = campaigns
                result['pagination'] = json.dumps({
                    'perPage' : per_page,
                    'currentPage' : page,
                    'total' : total
                })

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result), 200


@bp_dashboard.route('/campaigns/get', methods=['POST'])
@auth_required
def get_campaign_by_id():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : '',
        'campaign' : '',
        'modified_fields': json.dumps(modified_fields_on_edit)
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")


            if not campaign.valid_funnel():
                modified_fields_on_edit['funnel'] = True
                modified_fields_on_edit['credentials'] = True

            #check that the list has prospects and funnel exists
            
            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['campaign'] = json.dumps(campaign_dict)
            result['modified_fields'] = json.dumps(modified_fields_on_edit)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)



@bp_dashboard.route('/campaigns/create', methods=['POST'])
@auth_required
def create_campaign():
    current_user = g.user

    result = {
        'code' : -1,
        'msg' : '',
        'added' : ''
    }
    if request.method == 'POST':
        try:
            raw_data = request.form.get('_add_campaign', '')
            if not raw_data:
                raise Exception("There is no _add_campaign")
            
            campaign_data = JSCampaignData(raw_data=raw_data)

            funnel_id = campaign_data.funnel()
            funnel = shared.Funnel.objects(id=funnel_id).first()
            if not funnel:
                raise Exception("No such funnel")

            credentials = campaign_data.credentials()
            if not credentials:
                raise Exception("Credentials can't be empty")
        
            prospects_list = ProspectsList.objects(owner=current_user.id, id=campaign_data.prospects_list()).first()
            if not prospects_list:
                raise Exception("There is no such prospects list")
            
            create_fields = Campaign.get_create_fields()
            new_campaign = Campaign.async_create(owner=current_user.id, 
                                                campaign_data=campaign_data,
                                                create_fields=create_fields)
            if not new_campaign or not new_campaign.id:
                raise Exception("Something went wrong contact support.")

            #Already reloaded in async_create
            #new_campaign.reload()
            
            #assign prospects
            prospects = Prospects.objects(owner=current_user.id, assign_to_list=prospects_list.id)
            if prospects:
                ids = []
                need_data = new_campaign.need_contacts()
                for p in prospects:
                    tags = p.has_all_data(need_data)
                    if tags:
                        p.add_tags(tags)
                        continue

                    ids.append(p.id)
                if ids:
                    Prospects._assign_campaign_on_create(owner_id=current_user.id, campaign_id=new_campaign.id, prospects_ids=ids)

            campaign_dict = to_json_deep_dereference(new_campaign)

            result['code'] = 1
            result['added'] = json.dumps(campaign_dict)
        except Exception as e:
            #TODO: change to loggin
            print(e)
            traceback.print_exc()

            result['code'] = -1
            result['msg'] = 'SERVER ERROR: ' + str(e)

    return jsonify(result)

@bp_dashboard.route('/campaigns/edit', methods=['POST'])
@auth_required
def edit_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : '',
        'updated' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_di")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            if campaign.inprogress():
                raise Exception("Campaign in progress: stop progress first")
            
            raw_modified_fields = request.form.get('_modified_fields', '')
            if not raw_modified_fields:
                raise Exception("Bad _modified_fields")


            modified_fields = json.loads(raw_modified_fields)
            if not modified_fields:
                raise Exception("_modified_fields missed: don't know what to modify")

            raw_data = request.form.get('_add_campaign', '')
            if not raw_data:
                raise Exception("_add_campaign missed: don't know what to modify")
            
            campaign_data = JSCampaignData(raw_data=raw_data)

            edit_fields = [k for k, v in modified_fields.items() if v]
            if not edit_fields:
                raise Exception("edit_fields can't be empty")  

            campaign.async_edit(owner=current_user.id, campaign_data=campaign_data, edit_fields=edit_fields)

            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['updated'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/campaigns/delete', methods=['POST'])
@auth_required
def delete_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            scheduler.Scheduler.safe_delete_campaign(owner_id=current_user.id, campaign=campaign)

            result['code'] = 1
            result['msg'] = 'Success'
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/campaigns/start', methods=['POST'])
@auth_required
def start_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            
            scheduler.Scheduler.safe_start_campaign(owner=current_user.id, campaign=campaign)
            campaign.reload()
            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['campaign'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)


@bp_dashboard.route('/campaigns/pause', methods=['POST'])
@auth_required
def pause_campaign():
    current_user = g.user

    result = {
        'code' : 1,
        'msg' : ''
    }

    try:
        if request.method == 'POST':
            campaign_id = request.form.get('_campaign_id','')            
            if not campaign_id:
                raise Exception("Bad campaign_id")

            campaign = Campaign.objects(owner=current_user.id, id=campaign_id).first()
            if not campaign:
                raise Exception("No such campaign")

            
            scheduler.Scheduler.safe_pause_campaign(campaign=campaign)
            campaign.reload()
            campaign_dict = to_json_deep_dereference(campaign)

            result['code'] = 1
            result['msg'] = 'Success'
            result['campaign'] = json.dumps(campaign_dict)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result)
