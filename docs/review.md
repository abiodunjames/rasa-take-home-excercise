
If you want to run the code locally, make sure to run python 3 and install:
_Python Recommended: Execute in an isolated (virtual) environment. Tools: venv, pipenv_

_Tip: If Python 3 and above, you may want to leverage static types in your functions._

```
pip install flask aiohttp
git clone git://github.com/lucasicf/dict2xml.git
cd dict2xml
python setup.py install
```
The dict2xml and aiohttp dependencies will be newly introduced by the change request.
```python
import aiohttp
import asyncio
import async_timeout
from flask import Flask, request, abort


loop = asyncio.new_event_loop() # see my comment below

app = Flask(__name__)

# Please remove async from this method
async def incoming_2_outgoing_payload(payload):
    """Convert json to xml."""
    from decoder import Dict2XML
    # need to convert int keys to str, dict2xml can't handle int values
    return Dict2XML().parse({
        "vacation": {k: str(v) for k, v in payload.items()}})


async def fetch(url, payload):
    # don't use print. use Logger from Python. https://docs.python.org/3/howto/logging.html
    print("Triggering url {}".format(url))
    body = incoming_2_outgoing_payload(payload)

    async with aiohttp.ClientSession() as session, \
            async_timeout.timeout(10):
        async with session.post(url, data=body) as response:
            return await response.text()
    return None


def notified(responses):
    return "I notifed everyone - you are ready to go on vacation 🏖"


def ensure_future(tasks):
    """
    May be some comment here.
    In Python comments, it is standard to add argument and return types.
    IntelliJ makes this very simple to do.
    """
    if not asyncio.futures.isfuture(tasks):
        return None
    return asyncio.gather(tasks)


def is_valid_vacation_request(payload):
    return (payload["employee"] is not None and
            payload["end"] > payload["start"])


@app.route("/health")
def health():
    return "Ok"


@app.route("/vacation", methods=["POST"])
def index():
    """Employe can send a webrequest to this endpoint to request vacation.

    The request will be forwarded to internal systems to register the
    vacation. The format of the reuqest should be

    Example:
        $ curl \
            -XPOST \
            -H "Content-Type: application/json" \
            localhost:5000/vacation \
            -d '{"employee":"tom", "start": 1549381557, "end": 1549581523}'

    """

    payload = request.json
    if not is_valid_vacation_request(payload):
        abort(404, "Invalid vacation request!")

    # perform multiple async requests concurrently
    # to notify webhooks
    responses = loop.run_until_complete(asyncio.gather(
        fetch("https://api.hr-management.com/webhook", payload),
        fetch("https://api.hr-management.com/webhook", payload),
        fetch("https://api.sprintboard.com/notify", payload)
    ))

    # do something with the results
    return notified(responses)
 app.run(debug=False, use_reloader=False)
```

### Code Review

You're likely using Flask version >= 1.0. The development server for Flask version >=1.0 has threaded mode enabled by default. With threaded set to True, requests are each handled in a new thread.

If you disable threading as shown below, Flask development server will run in a single threaded mode and requests can wait in turn to be processed.

```python
    app.run(debug=False, threaded=False, use_reloader=False)
```

>
>
> Note: Flask development server is for development environment. In production, this code should be run under a proper WSGIs (Gunicorn) capable of handling concurrent requests

[`new_event_loop()`](https://docs.python.org/3.6/library/asyncio-eventloops.html) requires  you need to explicitly call `set_event_loop()` for the current context unlike the `get_event_loop()`

I would change line 8 to:

```python
loop = asyncio.get_event_loop()
```

I'm assuming you want to log  some info with  `    print("Triggering url {}".format(url))`  here. We should configure a standard logger.

```python
  logger.info(f"Triggering url :{url}")
```

The `responses` argument in the function `notified()` is not used. Please, remove it.

Please install `dict2xml` with pip.

```python
pip install dict2xml
```

For the `fetch()` method, Invalid or unreachable URLs will raise exceptions and we should handle them gracefully.

Please remove `async` from `incoming_2_outgoing_payload(payload)`

It's better to use swagger to document APIs. Could you please use swagger?
