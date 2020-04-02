import unittest
import os
import o24.config as config
from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, TaskLog
from o24.backend import app
from o24.backend import db
from o24.backend.models.shared import Action, Funnel
from o24.backend.utils.funnel import construct_funnel
from o24.globals import *

class TestBulkUpdates(unittest.TestCase):
    def test_1_bulk_update(self):
        return 

        Prospects.objects().update(status=NEW)

        new = Prospects.objects(status=NEW).all()
        print("*** Before update:{0}".format(len(new)))

        ids = Prospects.objects(status=NEW).update(status=IN_PROGRESS, full_result=True)
        print(dir(ids))
        print(ids.upserted_id)
        new = Prospects.objects(status=NEW).all()
        print("*** After update:{0} ids:{1}".format(len(new), ids))

    def test_2_unique_index(self):
        return 

        #one = TaskLog("three", "two")
        #one.save()

def setUpModule():
    env = os.environ.get('APP_ENV', None)
    assert env == "Test", "ERROR: Must be Test environment. APP_ENV={0}".format(env)

    settings = config.MONGODB_SETTINGS
    db_name = settings.get('db', None)
    assert db_name == "O24Mc-test", "ERROR: db_name. db_name={0}".format(db_name)

if __name__ == '__main__':
    unittest.main()
        

