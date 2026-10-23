# Weekly Announcements
* **MP1 Grade** will be posted soon (no later than tomorrow)
    * 4 WSUs (400 pts) + 1 check-off meeting (600pts)
* **MP2** is posted on Canvas under **Assignments**.
    * MP2-Part 1 is available. 
* **MP2-WSU 1** is is due TODAY (Friday, 10/23).
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 



## MP2-WSU 1
If you’re ready and would like to complete it now, feel free to do so. 

---

# Class 13: Async, File Uploads, and HTTP Errors

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain why `async` and `await` are used and apply them when reading an uploaded file.
2. Accept and read a CSV upload.
3. Convert expected Python errors into HTTP responses.
4. Store and retrieve uploaded movie datasets in memory.


---

# Before We Begin

Go to `class-exercise` and activate the virtual environment.

Install python-multipart for file uploads and update requirements:

```bash
python -m pip install python-multipart
python -m pip freeze > requirements.txt
```

---

# Part 1: Recap and Today's focus

Last class, we worked with individual movie records and learned how clients and servers exchange data through JSON requests and responses.

Today, we’ll learn how to upload files, such as CSV datasets. Other real-world examples of file upload include a photo-editing app uploading an image for background removal or a PDF converter processing a document and returning the converted PDF.



---

# Part 2: File Uploads

## In this course

We will use `async def` for file uploads that call await file.read(), and regular `def` for the other endpoints.

| Choice | Situation |
| --- | --- |
| `async def` | File upload: uses `await file.read()`. |
| `def` | Health, movie lookup, dataset retrieval, and processing: use synchronous code. |

> We use relatively small datasets locally, so you may not notice a performance difference in this course. Learning `async` and `await` prepares you to build applications that serve many users and wait for external APIs or databases.


## Async (quiz)

In programming, `async` allows a program to work on other tasks while waiting for a task to finish, instead of blocking everything until that task completes.

### Why Use Async?

Suppose an endpoint is waiting for an operation to finish, such as reading a file or receiving a response from another service. With `await`, the endpoint can pause while the server handles other requests. 

For example, if the operation takes 15 seconds, the server can handle other requests during that wait. Once the result is ready, the endpoint can continue.


### Waiting and Other Work

```python
async def demo_upload_csv(file):
    contents = await file.read()
    return contents
```

* `async def` defines an asynchronous function.
* `await` waits for an asynchronous operation to finish and allows other work to proceed if the operation pauses.
* Execution continues on the next line after the result is available.

Async helps with waiting; it does not make computation faster.

### In the real world

`async` and `await` are commonly used for operations that involve waiting:
- External API calls: Waiting for a payment or AI service to respond.
- Database queries: Waiting for results through an asynchronous database library.
- Real-time chat: Waiting for messages while serving other connected users.
- File transfers: Handling uploads or downloads while other requests proceed.




## Add a file-upload endpoint to the API

Add this endpoint:

```python
# main.py

from fastapi import File, UploadFile

@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}
```

Here, `await` waits for the uploaded file to be read. If the operation pauses while waiting, the server can handle other requests. Small files may be read almost immediately.

* `UploadFile` provides the uploaded file and metadata.
* `File(...)` declares a required upload.
* `file.filename` is its original filename.
* `await file.read()` returns its contents as bytes.

The upload arrives as multipart form data rather than a JSON request body. In `/docs`, the endpoint provides a file selector.

Check the endpoint: 

Use `http://127.0.0.1:8000/docs` after running:

```bash
python -m uvicorn main:app --reload
```

## Parsing the CSV

The following snippet shows how to read the uploaded _bytes_ into a DataFrame. You will use it inside the endpoint in the exercise.

```python
import io
import pandas as pd

contents = await file.read()
df = pd.read_csv(io.BytesIO(contents))
```

`await file.read()` returns the uploaded file’s contents as bytes (e.g., `b"title,year\nMovie A,2020\n"`). `io.BytesIO(contents)` wraps those bytes in an object that pandas can read like a file.

---

# Part 3: HTTP Errors

When an error occurs in a command-line program, we might log an error and exit with status 1.

An API, on the other hand, should return an error response for the request while keeping the server available for other requests.

## 404 - Resource Not Found

Add this demo endpoint to `main.py` inside `class12-14`.

```python
from fastapi import HTTPException

@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException( status_code=404, detail="Movie not found")

    return movie
```

For a missing movie, the response is:

```json
{"detail": "Movie not found"}
```

Raising `HTTPException` stops that request's endpoint execution. It does not stop the server.

## 400 - Expected Parsing Errors

Catch the expected errors around parsing:

```python
try:
    df = pd.read_csv(io.BytesIO(contents))
except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
    logger.warning(f"Cannot read CSV: {error}")
    raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")
```

An empty file may raise `pd.errors.EmptyDataError`. A malformed CSV can raise `pd.errors.ParserError`; some files cannot be decoded.

---

# Part 4: Store Uploaded Data in Memory

An API may need to keep data after an upload so a later request can retrieve it. 

We can create a Python class to organize this storage.

Create `src/storage.py` and complete the two TODOs:

```python
import logging

logger = logging.getLogger(__name__)

class DataStorage:
    def __init__(self):
        self.datasets = {}
        self.counter = 0

    def save_data(self, df, filename):
        self.counter += 1
        dataset_id = self.counter

        # TODO 1: Store the following dictionary in self.datasets
        # using dataset_id as the key and the dictionary as the value:
        # {"filename": filename, "data": df.copy()}

        logger.debug(f"Stored dataset: id={dataset_id}, rows={len(df)}")
        return dataset_id

    def get_data(self, dataset_id):
        item = self.datasets.get(dataset_id)
        if item is None:
            logger.debug(f"Dataset not found: id={dataset_id}")
            return None
        logger.debug(f"Retrieved dataset: id={dataset_id}")

        # TODO 2: Return a copy of the DataFrame from item

        
```

* The dictionary maps an integer ID to a filename and DataFrame.
* `save_data()` assigns an ID and stores a copy of the data.
* `get_data()` returns a copy, so changing the returned DataFrame does not change stored data.

We will connect `DataStorage` to the API in the exercise: upload → storage → ID → later lookup. 

# Try It Yourself — Upload and Retrieve a Movie Dataset

Continue in `main.py` inside `class-exercise/class12_14/`. Keep the Class 12 movie endpoints and the demo endpoints unchanged. 

## 1. Add CSV Upload and Storage

1. Add this model to `src/models.py`:
(use the models from Class 12 as a reference)

```python
class CSVInfo(BaseModel):
    # TODO 1: filename (str), rows (int), columns (int),
    # column_names (list[str]), dataset_id (int)
    pass
```

2. Add imports for `CSVInfo` and `DataStorage` to `src/__init__.py`.

3. Import them in the API module. 

4. Create `storage = DataStorage()`, outside the endpoints. Creating it inside an endpoint would create fresh storage for each call.

5. Add a new `POST /inspect-csv` endpoint using the following starter code and complete the TODOs. 

```python
from pathlib import Path

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    # TODO 2: check the filename extension using pathlib.
    # Reject non-CSV files with status 400 and log a WARNING.

    # TODO 3: await the file contents and parse the CSV.
    # Catch expected parsing/decoding errors (e.g. EmptyDataError,ParserError, UnicodeDecodeError) and raise HTTPException
    # with status_code=400.

    # TODO 4: save the DataFrame with storage.save_data().
    # Log the dataset ID, filename at INFO.
    # Return a CSVInfo object with the ID, filename, shape, and column names.
    pass
```

## 2. Add Dataset Lookup

Complete the starter code below. Use the Part 3 HTTP-error example as a reference for missing IDs.

```python
@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    # TODO 5: get the DataFrame using storage.get_data().
    # If it is missing, log a WARNING and raise HTTPException with status 404.
    # Otherwise, log successful retrieval at INFO.
    # Return a dictionary with dataset_id, rows, and columns.
    pass
```

## 3. Run and Check

```bash
python -m uvicorn main:app --reload
```

Use `http://127.0.0.1:8000/docs` to check:

* Health: 200 with status ok, including after an invalid request.
* Select the existing `messy_netflix_titles.csv` from its current location in `class-exercise` when uploading: 200 with its ID and metadata. Compare its shape and columns with pandas.
* Use the returned ID with `GET /datasets/{dataset_id}/shape`: matching row and column counts. A nonexistent ID should return 404.
* Upload `requirements.txt` from the parent `class-exercise` directory or an empty CSV: 400. Create an empty `empty.csv` for this check, then delete it.

Open `http://127.0.0.1:8000/datasets/abc/shape` directly in a browser to see a 422 response; `/docs` may reject the input before sending it.

### Example Responses and Logs

For illustration, uploading `example.csv` with columns `title` and `release_year` and two movie records returns:

```json
{"filename": "example.csv", "rows": 2, "columns": 2, "column_names": ["title", "release_year"], "dataset_id": 1}
```

Looking up that dataset's shape returns:

```json
{"dataset_id": 1, "rows": 2, "columns": 2}
```

Your Netflix filename and dimensions will differ. IDs depend on prior uploads and reset when the server restarts or reloads.

An empty CSV returns 400 with `{"detail": "Cannot read the uploaded CSV"}`. Application logs look like:

```text
10:15:02 INFO     main — Stored CSV: id=1, filename=example.csv
10:15:03 INFO     main — Retrieved dataset shape: id=1
10:15:04 WARNING  main — Dataset not found: 999
10:15:05 WARNING  main — Cannot read CSV: No columns to parse from file
```

## After Completing the Exercise

Save your work:

```bash
cd ..
git status
git add class12_14 requirements.txt
git commit -m "Add Class 13 async upload and HTTP error practice"
git push
```

---
