import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel, TaskQueue
from o24.backend.utils.funnel import construct_funnel
import random
import string
from flask import url_for
import json
from pprint import pprint
from bson.objectid import ObjectId

from o24.backend.google.models import GoogleAppSetting
from o24.production_tests.create_data import *

ERRORS = [
    {
        "status" : -1
    }
]

class SchedulerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_0_errors(self):
        while True:

            #Here we handle IN_PROGRESS and set ERRORS
            tasks = TaskQueue.objects(status=IN_PROGRESS)
            for task in tasks:
                task.status = -1


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
        
