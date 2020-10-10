"""FastAPI redis queue.

https://medium.com/@mike.p.moritz/using-docker-compose-to-deploy-a-lightweight-python-rest-api-with-a-job-queue-37e6072a209b
"""
__author__ = 'mangalbhaskar'


import time

def runTask(group_name, group_owner, group_description):
  print('starting runTask') # in place of actual logging
  
  time.sleep(5) # simulate long running task
  print('finished runTask')
  return {group_name: 'task complete'}
