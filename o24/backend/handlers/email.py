from o24.backend import celery
import o24.backend.scheduler.scheduler as scheduler
from flask import current_app
from o24.globals import *
import traceback
import time
import random
import o24.backend.models.shared as shared
from o24.exceptions.exception_with_code import ErrorCodeException

from o24.backend.gmail.controller import GmailController
from o24.backend.models.inbox.mailbox import MailBox
from o24.backend.handlers.email_senders import gmail_smtp, gmail_api, yandex_smtp, mailru_smtp

SEND_ACTION_HANDLERS = {
    'smtp' : gmail_smtp.send_email,
    'api' : gmail_api.send_email
}

CHECK_REPLY_ACTION_HANDLERS = {
    'smtp' : gmail_smtp.check_reply,
    'api' : gmail_api.check_reply
}


@celery.task
def email_check_reply(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in email_check_reply attempt")
            return 
        
        params = {}

        params['prospect_id'] = task.prospect_id
        params['campaign_id'] = task.campaign_id
        params['credentials_id'] = task.credentials_id
        if not params['credentials_id']:
            raise Exception("email_send_message ERROR: credentials_id can't be None for task_id:{0}".format(task_id))


        params['input_data'] = task.get_input_data()
        if not params['input_data']:
            raise Exception("INPUT_DATA ERROR: No input_data for task_id:{0}".format(task_id))
        
        params['credentials_data'] = params['input_data'].get('credentials_data', '')
        if not params['credentials_data']:
            raise Exception("INPUT_DATA.CREDENTIALS_DATA ERROR: No credentials_data for task_id:{0}".format(task_id))
        
        params['email_from'] = params['credentials_data'].get('email', '')
        if not params['email_from']:
            raise Exception("Can't find email_from for credentials task_id:{0}".format(task_id))

        params['parent_mailbox'] = MailBox.get_parent(prospect_id=task.prospect_id, 
                                        campaign_id=task.campaign_id)

        #ACTION BASED ON sender type
        sender = params['credentials_data'].get('sender', '')
        if not sender:
            raise Exception("Can't find sender for credentials task_id:{0}".format(task_id))

        handler = SEND_ACTION_HANDLERS.get(sender, None)
        if not handler:
            message = "Unsupported email sender={0}".format(sender)
            raise Exception(message)
        
        result_data = handler(task, **params)
        status = CARRYOUT
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''
        if (type(e) == ErrorCodeException):
            code = e.error_code
            raw = e.message

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock email_check_reply")
    return

@celery.task
def email_send_message(task_id):
    result_data = {
        'if_true' : False,
        'code' : -1,
        'error' : 'Unknown Error'
    }
    status = FAILED

    try:
        task = shared.TaskQueue.lock(task_id)
        if not task:
            print("CONCURRENCY in email_check_reply attempt")
            return 
        
        params = {}

        params['prospect_id'] = task.prospect_id
        params['campaign_id'] = task.campaign_id
        params['credentials_id'] = task.credentials_id
        if not params['credentials_id']:
            raise Exception("email_send_message ERROR: credentials_id can't be None for task_id:{0}".format(task_id))


        params['input_data'] = task.get_input_data()
        if not params['input_data']:
            raise Exception("INPUT_DATA ERROR: No input_data for task_id:{0}".format(task_id))
        
        params['credentials_data'] = params['input_data'].get('credentials_data', '')
        if not params['credentials_data']:
            raise Exception("INPUT_DATA.CREDENTIALS_DATA ERROR: No credentials_data for task_id:{0}".format(task_id))
        
        params['email_from'] = params['credentials_data'].get('email', '')
        if not params['email_from']:
            raise Exception("Can't find email_from for credentials task_id:{0}".format(task_id))

        params['parent_mailbox'] = MailBox.get_parent(prospect_id=task.prospect_id, 
                                        campaign_id=task.campaign_id)

        #ACTION BASED ON sender type
        sender = params['credentials_data'].get('sender', '')
        if not sender:
            raise Exception("Can't find sender for credentials task_id:{0}".format(task_id))

        handler = SEND_ACTION_HANDLERS.get(sender, None)
        if not handler:
            message = "Unsupported email sender={0}".format(sender)
            raise Exception(message)
        
        result_data = handler(task, **params)
        status = CARRYOUT
    except Exception as e:
        print(e)
        traceback.print_exc()

        status = FAILED
        code = -1
        raw = ''
        if (type(e) == ErrorCodeException):
            code = e.error_code
            raw = e.message

        result_data = {
            'error' : str(e),
            'code' : code,
            'raw' : raw
        }
            
    finally:
        if task:
            unlocked = shared.TaskQueue.unlock(task_id=task_id, result_data=result_data, status=status)
            if not unlocked:
                raise Exception("Can't unlock email_send_message")
    
    return