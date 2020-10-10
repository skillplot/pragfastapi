## FastAPI

There are many good writen matterial on internet about FastAPI and it's implementatio, projects.

Here, attempt is to put some handpicked references to help accelerate learning and adaption of FastAPI for the **Production grade API for machine learning**

* Why FastAPI
  * Auto documentation
  * Async/Await support, streaming support
  * Built-in validation and serialization
  * 100% type annotated so autocompletion works great
* Since FastAPI doesn't come with inbuilt service, you need to install uvicorn for it to run. uvicorn is an ASGI server which allows us to use async/await features.

* Installation
    ```bash
    pip install FastAPI
    pip install uvicorn
    ```
* Hello World
    ```bash
    from fastapi import FastAPI

    app = FastAPI()
    @app.get("/")
    async def root():
       return {"message":"Hello World"}
    ```
* Start server
    ```bash
    uvicorn hello:app --reload
    ```
* API auto documentation
    ```bash
    http://127.0.0.1:8000
    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/redoc
    http://127.0.0.1:8000/openapi.json
    ```
* [A basic introduction into FastAPI](https://medium.com/@abhishek_maheshwarappa/a-basic-introduction-into-fastapi-3b97157cabfb)
* [Official FastAPI documentation](https://fastapi.tiangolo.com/)  and [github repo](https://github.com/tiangolo/fastapi) is the best learning resource that is sufficient to learn about all the required nitty-grities.
* It uses some key fundamental python tech. If you are not aware of concept and the syntax of [python-types](https://fastapi.tiangolo.com/python-types/) or [async](https://fastapi.tiangolo.com/async/#in-a-hurry), this is essential to know these to be able to grasp the understanding of code base.
* Modern versions of Python have support for "asynchronous code" using something called "coroutines", with "async and await" syntax.
* When building APIs, you normally use these specific HTTP methods to perform a specific action.
    ```python
    @app.get('/')
    @app.post('/')
    @app.put('/')
    @app.patch('/')
    @app.delete('/')
    ```
  * "Operation" here refers to one of the HTTP "methods". One of:
    ```
    POST
    GET
    PUT
    DELETE
    # ...and the more exotic ones:

    OPTIONS
    HEAD
    PATCH
    TRACE
    ```
  * Normally you use:
    ```
    POST: to create data.
    GET: to read data.
    PUT: to update data.
    DELETE: to delete data.
    ```
  * So, in OpenAPI, each of the HTTP methods is called an "operation". The information here is presented as a guideline, not a requirement.


## WSGI vs ASGI; Gunicorn or Uvicorn; Flask or FastAPI

* The triplet combination is: WSGI/Gunicorn/Flask and ASGI/Uvicorn/FastAPI
* [uvicorn](https://www.uvicorn.org/)
* [FastAPI for Flask Users](https://amitness.com/2020/06/fastapi-vs-flask/)
* [Starlette](https://www.starlette.io/) is a lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services.


## References

* **Configuration**
  * [pydantic](https://pydantic-docs.helpmanual.io/) Data validation and settings management using python type annotations.
  * [FastAPISettings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
  * **How can I pass the configuration in the app?**
    * https://github.com/tiangolo/fastapi/issues/508
  * **Use Pydantic BaseSettings for config settings**
    * https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/87
  * **Storing object instances in the app context**
    * https://github.com/tiangolo/fastapi/issues/81
    * https://github.com/tiangolo/fastapi/issues/619
  * [pydantic Models](https://pydantic-docs.helpmanual.io/usage/models/#generic-models)
  * [Pedantic Configuration Management with Pydantic](https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html)
  * [Config from full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/core/config.py)
* **Misc**
  * [Official gitter chat channel](https://gitter.im/tiangolo/fastapi)
  * [Unify Python logging for a Gunicorn/Uvicorn/FastAPI application](https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/)
  * [why-we-switched-from-flask-to-fastapi-for-production-machine-learning](https://mc.ai/why-we-switched-from-flask-to-fastapi-for-production-machine-learning/)
  * [Alternatives, Inspiration and Comparisons](https://fastapi.tiangolo.com/alternatives/)
  * [migrate-from-flask-to-fastapi-smoothly](https://medium.com/better-programming/migrate-from-flask-to-fastapi-smoothly-cc4c6c255397)
  * [Simple Machine Learning Model Deployment using FastAPI](https://medium.com/@faisalmalikwidyaprasetya/simple-machine-learning-model-deployment-using-fastapi-5a6388db985f)
  * [Deploy a Machine Learning onnx Model on AWS using FastApi and Docker](https://medium.com/analytics-vidhya/deploy-a-machine-learning-onnx-model-on-aws-using-fastapi-and-docker-3872c17f99b5)
  * [cortexlabs/cortex](https://github.com/cortexlabs/cortex)
  * [FastAPI Production Deployment with Github actions & Dokku](https://blog.karmacomputing.co.uk/fastapi-production-deployment-with-dokku-and-github-actions/)
  * [Porting Flask to FastAPI for ML Model Serving](https://www.pluralsight.com/tech-blog/porting-flask-to-fastapi-for-ml-model-serving/)
  * [uvicorn Deployment](https://www.uvicorn.org/deployment/)
  * [Distributed task queue with Python using Celery and FastAPI](https://medium.com/@arocketman/distributed-task-queue-with-python-using-celery-and-fastapi-4cd1ad112c0f)
  * [Facade Method – Python Design Patterns](https://www.geeksforgeeks.org/facade-method-python-design-patterns/)
  * [Microservice in Python using FastAPI](https://dev.to/paurakhsharma/microservice-in-python-using-fastapi-24cc)
    * Introduction to Microservices - Microservice is the approach of breaking down large monolith application into individual applications specializing in a specific service/functionality. This approach is often known as Service-Oriented Architecture or SOA.
    * In monolithic architecture, every business logic resides in the same application. Application services such as user management, authentication, and other features use the same database.
    * In a microservice architecture, the application is broken down into several separate services that run in separate processes. There is a different database for different functionality of the application and the services communicate with each other using the HTTP, AMQP, or a binary protocol like TCP, depending on the nature of each service. Inter-service communication can also be performed using the message queues like RabbitMQ, Kafka or Redis.
    * Drawbacks of Microservice - The microservice architecture is not a silver bullet that solves all your problems, it comes with its drawbacks too. Some of these drawbacks are:
      * Since different services use the different database the transactions involving more than one service needs to use eventual consistency.
      * Perfect splitting of the services is very difficult to achieve at the first try and this needs to be iterated before coming with the best possible separation of the services.
      * Since the services communicate with each other through the use of network interaction, this makes the application slower due to the network latency and slow service.
    * Why Microservice in Python - Python is a perfect tool for building micro-services because it comes with a great community, easy learning curve and tons of libraries. Due to the introduction of asynchronous programming in Python, web frameworks with performance on-par with GO and Node.js, has emerged.
  * [Python 2020: Modern Best Practices](https://spiegelmock.com/2020/01/04/python-2020-modern-best-practices/)
  * [Build a FastAPI Server](https://python-gino.org/docs/en/master/tutorials/fastapi.html)
  * [Deploying Your Data Science Projects in JavaScript](https://rcd.ai/quick-deploy-react-visualization-python-json-api/)
  * [The open source stack for machine learning engineering](https://www.cortex.dev/)
    * As the field has matured, however, real infrastructure features—rolling updates, autoscaling, prediction monitoring, etc.—have gone from being “nice to haves” to being essential.
    * Run locally or host on your AWS account
    * Autoscaling
    * Spot instances
    * Rolling updates
    * Log streaming
    * Prediction monitoring
* **API Documentation**
  * [redoc](https://github.com/Redocly/redoc)
* **Streaming**
  * https://webrtchacks.com/webrtc-cv-tensorflow/
  * [Flask_Video_Streaming_for_Object_Detection](https://github.com/jiankaiwang/Flask_Video_Streaming_for_Object_Detection)
  * [cookiecutter](https://pypi.org/project/cookiecutter/)
  * [Machine learning model serving in Python using FastAPI and streamlit](https://davidefiocco.github.io/2020/06/27/streamlit-fastapi-ml-serving.html), [code ref](https://github.com/davidefiocco/streamlit-fastapi-model-serving/blob/master/fastapi/server.py)
* **FastAPI based projects / setup**
  * [project-generation](https://fastapi.tiangolo.com/project-generation/)
  * [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)
  * [full-stack-fastapi-couchbase](https://github.com/tiangolo/full-stack-fastapi-couchbase)
  * [uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)
  * [bigger-applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
  * [deploy-ml-fastapi-redis-docker](https://github.com/shanesoh/deploy-ml-fastapi-redis-docker)
  * [Deploy Machine Learning Models with Keras, FastAPI, Redis and Docker](https://medium.com/analytics-vidhya/deploy-machine-learning-models-with-keras-fastapi-redis-and-docker-4940df614ece)
  * [fastapi-nano](https://github.com/rednafi/fastapi-nano)
  * [Test-API](https://github.com/Atheuz/Test-API.git)
    * [from starlette.requests import Request](https://github.com/Atheuz/Test-API/blob/master/api/routers/basic.py#L11)
    * [result = request.app.redis.set(cat_id, to_set)](https://github.com/Atheuz/Test-API/blob/master/api/actions/storage.py#L14)
    * [factory pattern using FastAPI and Flask](https://github.com/Atheuz/Test-API/blob/master/api/factory.py)
    * http://0.0.0.0:8000/api/v1/docs
    ```bash
    pip install python-json-logger
    pip install python-dotenv
    pip install redis
    ```
  * [Ready-to-use and customizable users management for FastAPI](https://github.com/frankie567/fastapi-users)
  * [gino-starlette fastapi prod demo](https://github.com/python-gino/gino-starlette/tree/master/examples/prod_fastapi_demo)


## Snippets


* Imports
    ```python
    ## Flask
    from flask import Flask, request, jsonify, render_template, send_from_directory
    import random
    ## FastAPI
    from fastapi import FastAPI, Form, Request
    from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from pydantic import BaseModel
    import random
    import uvicorn
    ```
* Initialization
    ```python
    app = Flask(__name__)
    ##
    app = FastAPI()
    # optional, required if you are serving static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    # optional, required if you are serving webpage via template engine
    templates = Jinja2Templates(directory="templates")
    # depends on use cases
    class Item(BaseModel):
        language = 'english'
    app = FastAPI(title="DeepLabV3 image segmentation",
                  description='''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
                               Visit this URL at port 8501 for the streamlit interface.''',
                  version="0.1.0",
                  )
    ```
* Routing
    ```python
    from pydantic import BaseModel
    class Sentence(BaseModel):
        text: str

    @app.post('/lowercase')
    def lower_case(sentence: Sentence):
        return {'text': sentence.text.lower()}
    from typing import Dict

    @app.post('/lowercase')
    def lower_case(json_data: Dict):
        text = json_data.get('text')
        return {'text': text.lower()}


    app.include_router(users.router)

    app.include_router(
        items.router,
        prefix="/items",
        tags=["items"],
        dependencies=[Depends(get_token_header)],
        responses={404: {"description": "Not found"}},
    )

    ```
* `pydantic` Settings
    ```python
    from functools import lru_cache
    from typing import List

    from pydantic import BaseSettings


    class APISettings(BaseSettings):
        api_v1_route: str = "/api/v1"
        openapi_route: str = "/api/v1/openapi.json"

        backend_cors_origins_str: str = ""  # Should be a comma-separated list of origins

        debug: bool = False
        debug_exceptions: bool = False
        disable_superuser_dependency: bool = False
        include_admin_routes: bool = False

        @property
        def backend_cors_origins(self) -> List[str]:
            return [x.strip() for x in self.backend_cors_origins_str.split(",") if x]

        class Config:
            env_prefix = ""


    @lru_cache()
    def get_api_settings() -> APISettings:
        return APISettings()  # reads variables from environment
    ```
* Docker Compose
    ```
    version: '3'

    services:
      fastapi:
        build: fastapi/
        ports:
          - 8000:8000
        networks:
          - deploy_network
        container_name: fastapi

      streamlit:
        build: streamlit/
        depends_on:
          - fastapi
        ports:
            - 8501:8501
        networks:
          - deploy_network
        container_name: streamlit

    networks:
      deploy_network:
        driver: bridge
    ```