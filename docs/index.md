# Pragmatic FastAPI - Intro

The pragmatic FastAPI is the codebase for pragmatic python book series. These are opinionated fastapi practical examples. This is not the subsitute for basics on FastAPI documentations or other tutorials on internet.
This is instead consolidation of many practical use cases in the wild, broken down to simple use cases in an opinionated fashion.
This will be helpful for anyone who is started for the first time to attempt to build practical applications for production grade.

* Automatic Documentation - OpenAPI, JSON Schema, Swagger UI
* Pydantic - Validation, [Python Types (type hints, py 3.6+)](https://fastapi.tiangolo.com/python-types/), ORM, ODM
* Security and authentication - HTTP, OAuth2
* Starlette - Starlette is a lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services.
* [References](REFERENCES.md)


## Project Directory Structure

```bash
└── pragmatic-fastapi-dev
    ├── app
    │   ├── api
    │   ├── config
    │   ├── db
    │   ├── dnn
    │   │   └── gpuconfig
    │   ├── entities
    │   ├── routes
    │   ├── schemas
    │   ├── _site
    │   │   └── images
    │   ├── templates
    │   │   └── src
    │   ├── tests
    │   └── utils
    ├── data
    └── tests
        └── config
```

## Examples


**API Documentation**

* http://127.0.0.1:8000/docs
* http://127.0.0.1:8000/redoc
* http://127.0.0.1:8000/openapi.json


**Servers**

1. Hello World
  * http://127.0.0.1:8000
  * http://127.0.0.1:8000/hello/blah
  * http://127.0.0.1:8000/hello/dummy
  * http://127.0.0.1:8000/hello/dummy/age/99
  * http://127.0.0.1:8000/files//some/path/type/string
  * http://127.0.0.1:8000/dnnarch
  * http://127.0.0.1:8000/dnnarch?skip=3&limit=3&debug=true
    * debug = True/true/on/yes/1 or False/false/off/no/0
        ```bash
        bash start-hello.sh
        ```
2. Serving Static HTML Pages
  * http://127.0.0.1:8000
  * http://127.0.0.1:8000/site
  * http://127.0.0.1:8000/web/index.html
  * http://127.0.0.1:8000/web/websocket-1.html
    ```bash
    bash start-static.sh
    ```
3. Web-socket
  * http://127.0.0.1:8000
  * http://127.0.0.1:8000/site
  * http://127.0.0.1:8000/web/index.html
  * http://127.0.0.1:8000/web/websocket-1.html
  * http://127.0.0.1:8000/web/websocket-2.html
  * http://127.0.0.1:8000/web/websocket-3.html
    ```bash
    bash start-websocket.sh
    ```
4. Streaming - video, images, files, webcam
  * http://127.0.0.1:8000
  * http://127.0.0.1:8000/video
  * http://127.0.0.1:8000/cam
    ```bash
    bash start-stream.sh
    ```
5. Configuration and settings
  * http://127.0.0.1:8000
    ```bash
    bash start-config.sh
    ```


## Github pages site generation

* Install mkdocs
    ```bash
    pip install mkdocs
    ## search and install required plugins
    pip search mkdocs-
    ```
* Create / Update github page
    ```bash
    mkdocs gh-deploy --config-file ${PWD}/mkdocs.yml --remote-branch gh-pages
    ```
