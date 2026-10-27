# Weekly Announcements
* **MP2** is posted on Canvas under **Assignments**.
    * MP2-Parts 1 and 2 are available. 
* **MP2-WSU 2** is due on Friday (10/30) and will be available the night before.
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 
* **MP2 Push Day (Friday 10/30)**
    - We don't meet in class
    - 1:40pm-3:10pm
        - Srikar: https://teams.microsoft.com/meet/2281255279835743?p=ay3126mmOihpQPLw05
        - Sivapriya: https://teams.microsoft.com/meet/257018127590893?p=f47OQlMdiADSzoWguJ
    - 3:30pm-5:00pm
        - Srikar: https://teams.microsoft.com/meet/2693632704646782?p=JE1wbClWxCTiOUwZho
        - Sivapriya: https://teams.microsoft.com/meet/221577976042053?p=Uh6WETrW7msq7XZOtz

---

# Class 14: Config, Middleware, and API Tests

## Learning Objectives

By the end of today’s class, you will be able to:

1. Use Pydantic models to receive processing settings and control data processing.
2. Explain how middleware wraps an API request.
3. Add a request ID, status, and duration to a request log.
4. Log unexpected exceptions with traceback information.
5. Test an API using pytest and TestClient.

In `class-exercise`, activate the virtual environment

Install HTTPX for TestClient:

```bash
python -m pip install httpx2
python -m pip freeze requirements.txt
```
---

# Part 1: From Configuration to a Request Body

In data pipeline CLI tool, settings come from a YAML file. In API, the client sends settings in JSON. 

## 1. Define the Request Model

1. Add the following code to `src/models.py`. 

```python
from pydantic import BaseModel, Field

class ProcessingSettings(BaseModel):
    remove_duplicates: bool = True

class ProcessConfig(BaseModel):
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)
```

2. Add this import to `src/__init__.py`:

```python
from .models import ProcessConfig
```

## 2. Add an Endpoint

1. In `main.py`, import `ProcessConfig` and add this endpoint. 

```python
from src import ProcessConfig
import pandas as pd

@app.post("/demo/process-config")
def demo_process_config(config: ProcessConfig):
    df = pd.DataFrame({"title": ["Movie A", "Movie A", "Movie B", None]})
    settings = config.model_dump()

    if settings["processing"]["remove_duplicates"]:
        df = df.drop_duplicates()
        
    return {"rows": len(df)}
```

FastAPI validates the client's JSON and passes a `ProcessConfig` object to the endpoint. `model_dump()` converts it to a nested dictionary that our Python code can use.

Go to `http://127.0.0.1:8000/docs` after running:

```bash
python -m uvicorn main:app --reload
```

---

# Part 2: Middleware (quiz)

Some tasks are shared across multiple endpoints, such as logging response status codes, measuring request duration, and generating request IDs.

Middleware allows us to write this shared code once and apply it to requests across endpoints like `/health` and `/inspect-csv`.

An endpoint handles a specific operation (the client's request). Middleware runs around the request.

## Build a Small Example Together

Create `middleware.py` inside `class12_14/` and add:

```python
import logging

from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    # Before FastAPI handles the request:
    logger.info(f"Received: {request.method} {request.url.path}")

    # FastAPI handles the request
    response = await call_next(request)

    # After FastAPI produces a response:
    logger.info(f"Returned: status={response.status_code}")
    return response

```

* `request` represents the incoming HTTP request.
* `call_next(request)` passes it to the next application step, including routing, validation, and the matching endpoint when appropriate. 
* `return response` returns the response to the client after the middleware finishes its work.

| Expression | Example for a health request |
| --- | --- |
| `request.method` | `"GET"` |
| `request.url.path` | `"/health"` |
| `response.status_code` | `200` |


In the existing `main.py`, add the import at the top and register the middleware after creating `app`:

```python
from middleware import log_requests

# After the existing app = FastAPI(...):
app.middleware("http")(log_requests)
```

Run from `class-exercise/class12_14/`:

```bash
python -m uvicorn main:app --reload
```

In `http://127.0.0.1:8000/docs`, execute `GET /health`. The response body is still `{"status": "ok"}`, but the server terminal now includes:

```text
10:15:02 INFO     middleware — Received: GET /health
10:15:02 INFO     middleware — Returned: status=200
```

## Add a Request ID and Duration

A request ID identifies one request. It lets us match a client's response to its server log. For an ID and duration, we will use `time` and `uuid` modules.

Add these imports to `middleware.py`:

```python
import time
import uuid
```

Expand the existing `log_requests()` in `middleware.py` as follows. Keep the logger and imports in that module and the existing registration in `main.py`.

```python
async def log_requests(request: Request, call_next):
    # Before: identify the request and start the timer.
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    response = await call_next(request)

    # After: measure, log, and attach the response header.
    duration_ms = (time.perf_counter() - started) * 1000
    logger.info(f"request_id={request_id} {request.method} {request.url.path} status={response.status_code} duration={duration_ms:.1f}ms")
    response.headers["X-Request-ID"] = request_id
    return response
```

* `uuid.uuid4().hex[:8]` creates an eight-character ID for this exercise.
* `request.state.request_id` stores the ID on this request so other parts of application can access it.
* `response.headers["X-Request-ID"]` sends the same ID back to the client as response metadata. It does not add a field to the JSON body.
* `time.perf_counter()` measures elapsed time -- this records the start before `call_next()` and subtract it afterward, includijng time spent waiting.


Execute `GET /health` again. Compare the terminal log with **Server response → Response headers** in `/docs`:

```text
# Terminal:
10:15:02 INFO     middleware — request_id=a3f2c1d8 GET /health status=200 duration=1.2ms

# Response headers:
x-request-id: a3f2c1d8
```

The IDs must match for that request. Send it again: the new request gets a new ID. Header names are case-insensitive, so `/docs` may show lowercase names.

---

# Part 3: Unexpected Errors (quiz)

Call `GET /datasets/999/shape` for an ID that does not exist. FastAPI handles the endpoint's `HTTPException` and produces a `404` response (e.g., not found). The middleware receives that response after `await call_next(request)` and can inspect its status.

Similarly, an invalid path parameter produces `422`, and a rejected upload produces `400`. These handled errors do not normally enter the middleware's `except Exception` block.

The request-summary log level from the response status:

| Status | Request Log Level |
| --- | --- |
| Below 400 | INFO |
| 400–499 | WARNING |
| 500 and above | ERROR |


| 500-level Status Code | Meaning | Example |
| --- | --- | --- |
| 500 Internal Server Error	| An unexpected server error occurred. | An unhandled Python exception. |
| 502 Bad Gateway | A gateway received an invalid response from another server.	| An upstream server returns an invalid response. |
| 503 Service Unavailable | The server is temporarily unavailable. | Server overload or maintenance. |
| 504 Gateway Timeout | A gateway timed out waiting for another server. | An upstream server takes too long to respond. |

## 500: Catch an Unexpected Failure

An unhandled Python error, such as a programming error inside an endpoint, can interrupt `call_next()`. Wrap that operation as follows:

```python
try:
    response = await call_next(request)
except Exception:
    logger.error(f"Unexpected failure: request_id={request_id}",exc_info=True)
    response = JSONResponse(status_code=500,content={"detail": "Internal server error"})
```

Import `JSONResponse` from `fastapi.responses`. `exc_info=True` includes the exception and traceback in the server log; the client receives only the short error message.

Because both paths assign `response`, the code after this block can still calculate duration, log the status, attach the ID header, and return the response. The traceback log explains the failure; the request-summary log records the final `500` response.

This broad catch belongs at the request boundary. Continue catching specific expected errors near the operation that can fail inside individual functions.

---

# Part 4: Test the API with TestClient


A TestClient sends requests directly to the application during a test. You do not need to start Uvicorn.

Create `test_api.py` inside `class12_14/` and write the health-check test together. You will add one more test to this same file in TIY:

```python
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Run:

```bash
python -m pytest test_api.py -v
```

Expect output similar to:

```text
test_api.py::test_health PASSED

1 passed
```


Compare this with the earlier pytest pattern:

* Arrange: create the client.
* Act: make the request.
* Assert: check the status and response content.

---

# Try It Yourself 

Continue in `class12_14/`. Extend the existing configuration model, demo processing endpoint, middleware, and tests.

## 1. Add a Missing-Value Setting

In `src/models.py`, extend `ProcessingSettings`:

```python
class ProcessingSettings(BaseModel):
    remove_duplicates: bool = True
    # TODO: Add drop_missing as a bool with default True.
```

In `main.py`, extend the existing `demo_process_config()` function. After the duplicate-removal step and before `return`.


Refresh `/docs` and execute `POST /demo/process-config` with:

```json
{
  "processing": {
    "remove_duplicates": true,
    "drop_missing": true
  }
}
```

Expect `{"rows": 2}`. Change the settings and check these results:

| remove_duplicates | drop_missing | Expected rows |
| --- | --- | --- |
| true | true | 2 |
| true | false | 3 |
| false | true | 3 |
| false | false | 4 |

## 2. Complete the Middleware

Add this import to middleware.py:
```python
from fastapi.responses import JSONResponse
```

Update the existing `log_requests()` function in `middleware.py` and complete the TODOs below.

```python
async def log_requests(request: Request, call_next):
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    # TODO 1: Use the try/except block from Part 4
    # to handle the request and assign response.

    duration_ms = (time.perf_counter() - started) * 1000
    message = (
        f"request_id={request_id} {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration_ms:.1f}ms"
    )

    # TODO 2: Log message at INFO for status < 400 (e.g. logger.info(message)),
    # WARNING for 400–499, and ERROR for status >= 500.

    response.headers["X-Request-ID"] = request_id
    return response
```

## 3. Add One More Test

Keep the `client` fixture and `test_health()` from Part 5 in `test_api.py`. Add the following test below them and complete the TODO:

```python
def test_requests_have_different_ids(client):
    # TODO: send two GET /health requests.
    # Assert that their X-Request-ID header values are different.
    pass
```

Run both tests:

```bash
python -m pytest test_api.py -v
```


## 4. Observe the Requests

Restart the server:

```bash
python -m uvicorn main:app --reload
```

In `/docs`, call:

1. `GET /health` — 200;
2. `GET /datasets/999/shape` — 404;
3. Open `http://127.0.0.1:8000/datasets/abc/shape` directly in your browser — 422. The `/docs` form may reject non-integer input before sending it.

Inspect the response headers and the terminal logs. Each response should include `X-Request-ID`. Its value should match the ID in that request’s summary log.

## Expected Results

In `/docs`, expand **Server response → Response headers** after executing `GET /health`. Expect status 200 and:

```json
{"status": "ok"}
```

The response headers include an ID, for example:

```text
x-request-id: a3f2c1d8
```

Header names are case-insensitive, so `/docs` may display `X-Request-ID` in lowercase. The matching application log looks like:

```text
10:15:02 INFO     middleware — request_id=a3f2c1d8 GET /health status=200 duration=1.2ms
10:15:03 WARNING  middleware — request_id=b4e3d2c9 GET /datasets/999/shape status=404 duration=0.8ms
10:15:04 WARNING  middleware — request_id=c5f4e3da GET /datasets/abc/shape status=422 duration=0.6ms
```

IDs, timestamps, and durations will vary. The existing endpoints and Uvicorn may print additional logs. Each response's ID must match its own request-summary log.

Both tests should pass; the summary will include:

```text
2 passed
```

## After Completing the Exercise

Save your work:

```bash
# in the class-exercise directory:
git status
git add class12_14 requirements.txt
git commit -m "Add Class 14 request logging and API tests"
git push
```

---