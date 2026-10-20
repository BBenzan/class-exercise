# Weekly Announcements
* **MP2** is posted on Canvas under **Assignments**.
    * MP2-Part 1 is available. 
* **MP2-WSU 1** is due on Friday (10/23) and will be available the night before.
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 
* Are you interested in **graduate school**? -- https://www.khoury.northeastern.edu/event/boston-on-campus-graduate-fair-fall-2026/

---

# Class 12: FastAPI Fundamentals

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain how an API connects a client to application code.
2. Create and run a local FastAPI application.
3. Define endpoints with path and query parameters.
4. Use Pydantic models for request and response data.
5. Send requests through the interactive API documentation.

> All exercises we do in Classes 12–14 are expected to be completed inside `class-exercise/class12_14/`, using the existing class-exercise virtual environment. 

---

# Part 1: From a Pipeline to an API (quiz)

So far, we have built a program when a user runs it from the command line.

Now, we will make those functions available through an API so that other applications, such as a website or mobile app, can request data processing and receive the results.

By the end of these API lessons, you will have built an application that receives requests from a client (e.g., another program), runs the appropriate code, and returns a response. For example, another application could upload a file to your API and retrieve the processed data.


| Component | Responsibility |
| --- | --- |
| Client | Sends a request |
| API server | Receives the request and calls application functions |
| Response | Returns a status code and data |


## Endpoint

Endpoint is a specific URL for API processing. It combines an HTTP method and a URL path to perform a specific job, such as retrieving or adding data.

Examples:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Check whether the application responds |
| `GET /movies` | Retrieve movies |
| `GET /movies/{movie_id}` | Retrieve one movie |
| `POST /movies` | Add a movie |

Put simply, use GET to retrieve data and POST to submit data for creation/processing

## Response
Response as JSON:

```json
{"id": 1, "title": "Movie A", "release_year": 2020}
```

---

# Part 2: FastAPI: Create and Run an Application

## What is FastAPI? (quiz)

FastAPI is a Python framework for building APIs -- it provides tools and a structure for building an application.

FastAPI connects HTTP requests to Python functions, validates request data, and returns responses. It also generates interactive documentation where you can try your endpoints.

We will use `FastAPI` to define the application and `Uvicorn` to run its server.

From `class-exercise`, install the packages in your active environment:

```bash
python -m pip install fastapi "uvicorn[standard]"
python -m pip freeze > requirements.txt
```

Create `class12_14/` inside `class-exercise`, then go to that directory

Create `main.py` and add:

```python
#main.py

from fastapi import FastAPI, Query

app = FastAPI(title="Movie API")


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

## The Endpoint Decorator

```python
#The decorator tells FastAPI: When a GET request arrives at `/health`, call the function directly below.

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

| Code | Meaning |
| --- | --- |
| `app` | Our FastAPI application |
| `.get()` | Register a function for GET requests |
| `"/health"` | The URL path the client requests |
| `health_check()` | The Python function that handles the request |

FastAPI registers this connection when the module is loaded. The function body runs when a client makes the matching request.

The function name does not determine the URL. The path in the decorator does.

For example, changing the decorator to `@app.get("/status")` would change the endpoint to `/status`, even if the function were still named `health_check`.

## Start the Server 

Running `python main.py` alone does not start this server.

From `class-exercise/class12_14/`, run:

```bash
python -m uvicorn main:app --reload
```

* `main` is the Python module name, without `.py`.
* `app` is the FastAPI object in that module.
* `--reload` restarts the server when code changes during development.

Keep this terminal running. Open a second terminal if you need other commands. Press `Ctrl+C` to stop the server.

In your web browser, go to: 

http://127.0.0.1:8000/health

Expected response:

```json
{"status": "ok"}
```

Note:
- FastAPI: Defines which code runs when a request arrives.
- Uvicorn: Starts the server, receives requests, and passes them to the FastAPI application.

## Interactive Documentation

The interactive documentation page will act as a client, allowing us to send requests to our API server and view its responses.

Open:

http://127.0.0.1:8000/docs

For an endpoint:

1. Expand it.
2. Select **Try it out**.
4. Select **Execute**.
5. Inspect the response code and response body.
    - Response code: 200
    - Response body: {"status": "ok"} 

FastAPI generates this page from your endpoint definitions and models. You can use it to send POST requests as well as GET requests.

## Status Codes

| Code | Meaning in Our Examples |
| --- | --- |
| 200 | Request succeeded |
| 400 | The application rejected a request |
| 404 | Requested resource was not found |
| 422 | Request data did not meet the declared input requirements |
| 500 | Unexpected server error |


---

# Part 3: Path and Query Parameters

## Path Parameters

Add this demo endpoint to `main.py`. Demo function names start with `demo_`, and their paths start with `/demo/` so they can remain alongside the TIY endpoints. 

```python
#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}
```


Refresh /docs and expand GET /demo/movies/{movie_id}.

1. Select Try it out, enter an integer, 2, for movie_id, and click Execute. 
    - Confirm status 200 and response body {"requested_id": 2}.
2. In your browser, go to http://127.0.0.1:8000/demo/movies/abc.
    - Inspect the validation error in the response and confirm status 422 in the Uvicorn log.


Summary: 

- `GET /demo/movies/2` -- FastAPI reads `2` from the path and passes it as the integer `movie_id`.
- A request to `/demo/movies/abc` produces a 422 response.


## Query Parameters

Add this endpoint to the same file:

```python
from fastapi import Query

#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}
```

Refresh /docs and expand GET /demo/movies.
1. Select Try it out, enter 1 for limit, and click Execute. 
    - Confirm status 200 and response body {"requested_limit": 1}.
2. In your browser, go to http://127.0.0.1:8000/demo/movies?limit=0. 
    - Inspect the validation error in the response and confirm status 422 in the Uvicorn terminal log.

summmary:
`GET /demo/movies?limit=1`
* The default is `2` when `limit` is omitted.
* `ge=1` means greater than or equal to one.
* `limit=0` produces a 422 response.


---

# Part 4: Request and Response Models with Pydantic

## Pydantic
Pydantic defines and validates the structure and types of data.

FastAPI uses Pydantic to validate the received JSON, creates a Pydantic object, and passes it to the endpoint.

We will create Pydantic models by inheriting from BaseModel. In other words, BaseModel handles initialization and validation using the fields we declare, so we do not need to write our own __init__() (e.g., Python class).

1. Create `src/` with `__init__.py` and `models.py`.

2. In `models.py`, add:

```python
from pydantic import BaseModel

class MovieInput(BaseModel):
    title: str
    release_year: int


class MovieResponse(MovieInput):
    id: int
```

`MovieResponse` inherits MovieInput and adds an ID.

The field declarations (e.g., title, release_year, id) use Python type annotations. Pydantic uses them to check the values.



3. In `src/__init__.py`, Add:

```python
from .models import MovieInput, MovieResponse
```

## Request Body Model 
The request body contains data sent by the client to the server. 

In our example, use `MovieInput` to define and validate the data received in the JSON request body.

Add the following endpoint to `main.py`:

```python
from src import MovieInput

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.
```

For example:

In /docs, expand POST /demo/movies, select Try it out, and enter this JSON request body:

```json
{"title": "Movie C", "release_year": 2022}
```

Confirm that the response code is 200 and the response body contains the same title and year.

What happened: FastAPI validates it and provides a MovieInput object to the endpoint:

```python
@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    # movie.title --> "Movie C"
    # movie.release_year --> 2022
    return movie.model_dump() #{"title": "Movie C", "release_year": 2022}
```

Try omitting `release_year` or using `"unknown"` for its value. The request should receive 422.

## Response Model 

The response model defines and validates the data returned by the server.

We use separate models because the client sends the title and year, while the server returns those fields along with a new ID.


1. Add this new endpoint to `main.py`:

```python
from src import MovieResponse

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record
```

Our endpoint code assigns the ID and stores the movie on the server. FastAPI validates the returned record using MovieResponse and sends it to the client as a JSON response.


We can return either one movie or a list of movies, using the matching response model:
```python
# response_model=MovieResponse: expects one movie.
return record

# response_model=list[MovieResponse]: expects a list of movies.
return [record]
```
---

# Try It Yourself — Build a Movie API

Continue inside `class-exercise/class12_14/`. Extend `main.py`; keep the health endpoint you created earlier.

The structure should be:

```text
class-exercise/
├── requirements.txt
└── class12_14/
    ├── main.py
    └── src/
        ├── __init__.py
        └── models.py
```

## 1. Logging and Starter Data Setup

Add logging and starter data in the API module:

```python
#main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}
```

This dictionary is temporary storage. It resets whenever the server restarts, including after a reload.

## 2. Complete the Endpoints

Keep the demo endpoints, including `GET /demo/movies/{movie_id}`. Class 13 will add movie lookup at `GET /movies/{movie_id}`.

Add separate `GET /movies` and `POST /movies` endpoints using the following TODOs. Keep the `/demo/` endpoints unchanged. 

```python
#main.py


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    # TODO 1: return up to limit movies as a list.
    # Log the number returned at INFO.
    # hint: movies is a dictionary whose values are movie records.
    pass


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    # TODO 2: 
    # Convert movie to a dictionary, add the new ID, and store it.
    # Log the new ID at INFO and return the stored record.
    pass
```

Import the models from `src`. The ID rule is sufficient here because this exercise has no deletion endpoint.


## Check the Results

Using `/docs`:

1. List movies with `limit=1`: expect only Movie A.
2. Add Movie C with year 2022: expect ID 3.
3. List movies with `limit=10`: expect all three movies.
4. Submit a movie without a year: expect 422.
5. List with `limit=0`: expect 422.

## Expected Responses and Logs

Start with the two starter movies and make these requests in order. Stored movies reset when the server restarts or reloads.

### 1. List One Movie — 200

`GET /movies?limit=1` returns a list containing Movie A:

```json
[
    {"title": "Movie A", "release_year": 2020, "id": 1}
]
```

### 2. Add a Movie — 200

Send this JSON body to `POST /movies`:

```json
{"title": "Movie C", "release_year": 2022}
```

The response is one movie, including its new ID:

```json
{"title": "Movie C", "release_year": 2022, "id": 3}
```

### 3. List All Three Movies — 200

`GET /movies?limit=10` returns:

```json
[
    {"title": "Movie A", "release_year": 2020, "id": 1},
    {"title": "Movie B", "release_year": 2021, "id": 2},
    {"title": "Movie C", "release_year": 2022, "id": 3}
]
```

### 4. Invalid Requests — 422

* Submit `{"title": "Movie D"}` to `POST /movies`: the response reports that `release_year` is required.
* Open `http://127.0.0.1:8000/movies?limit=0` directly in your browser: the response reports that `limit` must be at least 1.

The response body contains a `detail` list describing the validation errors. The `/docs` form may reject an invalid query value before sending a request; use the direct URL above to observe the server's 422 response.

### Terminal Logs

The three successful requests above produce application messages similar to:

```text
10:15:02 INFO     main — Returned 1 movies
10:15:03 INFO     main — Added movie: id=3
10:15:04 INFO     main — Returned 3 movies
```

Timestamps will differ. Uvicorn also prints server and access logs, including response status codes. FastAPI rejects invalid inputs before calling the endpoint function, so those 422 requests do not produce the function's success log.

## After Completing the Exercise

Save your work:

```bash
cd ..
git status
git add class12_14 requirements.txt
git commit -m "Add Class 12 FastAPI practice"
git push
```