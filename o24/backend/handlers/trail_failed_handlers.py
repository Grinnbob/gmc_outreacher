import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q

def system_error(task):
    if not task:
        print("system_error: task is None")
        return
  
    result_data = task.result_data
    print("system_error: can't fix for task.id={0} result_data={1}".format(task.id, result_data))

