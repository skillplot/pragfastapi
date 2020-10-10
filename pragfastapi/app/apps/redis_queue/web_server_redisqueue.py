"""FastAPI redis queue.

https://medium.com/@mike.p.moritz/using-docker-compose-to-deploy-a-lightweight-python-rest-api-with-a-job-queue-37e6072a209b
"""
__author__ = 'mangalbhaskar'


from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from redis import Redis
from rq import Queue
from worker import runTask


## Request body classes
class Group(BaseModel):
  owner: str
  description: str = None


app = FastAPI()


redis_conn = Redis(host='my_redis', port=6379, db=0)
q = Queue('my_queue', connection=redis_conn)


@app.get('/hello')
def hello():
  """Test endpoint"""
  return {'hello': 'world'}


@app.post('/groups/{group_name}', status_code=201)
def addTask(group_name: str, group: Group):
  """
  Adds tasks to worker queue. 
  Expects body as dictionary matching the Group class.
  """
  if group_name not in ('group1', 'group2'):
      raise HTTPException(
          status_code=404, detail='Group not found'
      )
  job = q.enqueue(
              runTask,
              group_name, group.owner, group.description
          )
  return {'job': job}
