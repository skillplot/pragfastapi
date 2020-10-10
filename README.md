# Pragmatic FastAPI

This is the part of my `Pragmatic Python` book series. `Pragmatic` book series are opinionated practical mini projects, tutorials, development environment setup and project structure.

Mini projects are more the toy examples and can be thought of small tools that can be extended to fit into the production grade pipeline.

Web: [skillplot.github.io/pragfastapi](https://skillplot.github.io/pragfastapi/)

* [References](REFERENCES.md)


## Project Directory Structure

```bash
pragfastapi/
├── app
│   ├── api
│   ├── apps
│   │   ├── redis_queue
│   │   ├── sql_app
│   │   └── sql_app_alembic
│   │       └── alembic
│   │           └── versions
│   ├── config
│   ├── db
│   ├── dnn
│   │   └── gpuconfig
│   ├── entities
│   ├── routes
│   ├── schemas
│   ├── _site
│   │   ├── css
│   │   └── images
│   ├── templates
│   │   └── src
│   ├── tests
│   │   └── config
│   └── utils
├── bk
│   └── app
│       ├── api
│       ├── routes
│       └── utils
└── data
    ├── images -> local/images
    ├── local
    │   ├── images -> ${HOME}/Pictures
    │   └── videos
    └── videos
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


