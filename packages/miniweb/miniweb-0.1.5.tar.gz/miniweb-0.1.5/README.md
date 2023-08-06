# miniweb

A simple web framework for Python.

## Example 1. Working with gunicorn.

*/path/to/your/project/debugserver.py*

```
from miniweb import Application
from miniweb import simplejson_api

@simplejson_api
def ping(http_request, http_response):
    return "pong"

@simplejson_api
def echo(http_request, http_response):
    return http_request.GET.get("msg", "")

application = Application()
application.router.add_route("/ping", ping)
application.router.add_route("/echo", echo)
```

*/path/to/your/project/wsgi.conf.py*

```
bind = ["0.0.0.0:9132"]
workers = 4
threads = 32
daemon = True
errorlog = "logs/gunicorn.error.log"
keepalive = 300
timeout = 300
graceful_timeout = 300
loglevel = "info"
```

*start.sh*

```
#!/bin/bash
cd /path/to/your/project/
gunicorn --config=wsgi.conf.py --pidfile=/path/to/your/project/gunicorn.pid debugserver:application
```

*After debugserver start, start ipython and do requests*

```
In [14]: import requests

In [15]: requests.get('http://127.0.0.1:9132/ping').json()
Out[15]: {'success': True, 'result': 'pong', 'error': {'code': 0, 'message': 'OK'}}

In [16]: requests.get('http://127.0.0.1:9132/echo?msg=hello').json()
Out[16]: {'success': True, 'result': 'hello', 'error': {'code': 0, 'message': 'OK'}}
```

## Example 2. Working with gevent.pywsgi.

*/path/to/your/project/debugserver.py*

- Server code is the same with the server code using gunicorn.

*start.sh*

```
#!/bin/bash
cd /path/to/your/project/
python -m gevent.pywsgi -b 0.0.0.0:9132 debugserver:application
```

*After debugserver start, start ipython and do requests*

```
In [14]: import requests

In [15]: requests.get('http://127.0.0.1:9132/ping').json()
Out[15]: {'success': True, 'result': 'pong', 'error': {'code': 0, 'message': 'OK'}}

In [16]: requests.get('http://127.0.0.1:9132/echo?msg=hello').json()
Out[16]: {'success': True, 'result': 'hello', 'error': {'code': 0, 'message': 'OK'}}
```

## How to write a request handler?

```
def ping(http_request:HttpRequest, http_resposne:HttpResponse) -> None:
    http_resposne.response("pong")
```

1. A handle is a callable object and always takes two parameters: http_request and http_resposne.
1. The parameter http_request holds all information about the request, e.g. META, GET, POST, COOKIES and FILES...
1. The parameter http_resposne is used to handle all response things, e.g. status_code, response_content, response_headers, response_cookies...
1. The handler returns nothing, and all things returned will be discarded, all response things should done by http_response methods.

# What is SAPIs (Simple APIs)?

1. miniweb.sapi decorators help you make a json or jsonp response easily.
1. Instead of set response content by http_response methods, with miniweb.sapi you just returns response data from the handler function, and the SAPIs decorator will call http_response methods for your. For example:
    ```
    # ###################################################################
    # Inside the handle we just returns the core result "pong",
    # but simplejson_api will do the result pack for you,
    # so that you get the final result:
    # {
    #     "success": True,
    #     "result": "pong",
    #     "error": {
    #         "code": 0,
    #         "message": "OK",
    #     }   
    # }
    # ###################################################################
    @simplejson_api
    def ping(http_request:HttpRequest, http_resposne:HttpResponse):
        return "pong"

    ```

## Releases

### v0.1.5 

- First release.
- Core dispatch and router dispatch are ready.
- HttpRequest and HttpResponse are ready.
- SimpleAPI decorators are eady.
- @TODO: `multipart/form-data` content type is NOT supported yet.