## Copyright (c) 2020 mangalbhaskar.
"""FastAPI background task.

https://fastapi.tiangolo.com/tutorial/background-tasks/
https://www.starlette.io/background/

If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery.

http://www.celeryproject.org/

They tend to require more complex configurations, a message/job queue manager, like RabbitMQ or Redis, but they allow you to run background tasks in multiple processes, and especially, in multiple servers.
https://fastapi.tiangolo.com/project-generation/

But if you need to access variables and objects from the same FastAPI app, or you need to perform small background tasks (like sending an email notification), you can simply just use BackgroundTasks.
"""
__author__ = 'mangalbhaskar'
__credit__ = 'fastapi.tiangolo.com'


from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


## And as the write operation doesn't use async and await, we define the function with normal def:
def write_notification(email: str, message=""):
  with open("log.txt", mode="w") as email_file:
    content = f"notification for {email}: {message}"
    email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
  background_tasks.add_task(write_notification, email, message="some notification")
  return {"message": "Notification sent in the background"}




def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
  if q:
    message = f"found query: {q}\n"
    background_tasks.add_task(write_log, message)
  return q


@app.post("/send-notification-2/{email}")
async def send_notification_depends(
  email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
  message = f"message to {email}\n"
  background_tasks.add_task(write_log, message)
  return {"message": "Message sent"}

