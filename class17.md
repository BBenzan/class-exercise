# Weekly Announcements

* **MP3** is posted on Canvas under **Assignments**.
    * MP3-Part 1 is available. 
* **MP3-WSU 1** is is due TODAY (Friday, 11/6).
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 
* **Next Week**: 
    * Tuesday: Regular Lecture with Quiz 9, and
    * Friday: MP3 Push Day, online Support (no in-person class this day) 

---

# Class 17: Connect SQLite to an API and Test Database Behavior

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain how transactions protect related database changes.
2. Connect API endpoints to reusable SQLite storage methods.
3. Retrieve and add stored records through GET and POST, and handle missing resources.
4. Test database persistence and transaction rollback using temporary files.


---

# Part 0: Recap on `BookStorage`

---

# Part 1: Keep Related Changes Together (quiz)

A **transaction** groups database changes into one unit: either all changes are saved with `commit()`, or all changes are undone if we call `rollback()`.

Real examples include: Bank transfer (e.g., update one account to subtract money; update another to add it), Placing an order (e.g., insert the order; update inventory to reduce stock).

Add this provided method inside `BookStorage`:

```python
    def replace_books(self, books):
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = "DELETE FROM books"
            connection.execute(sql_statement)
            sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
            connection.executemany(sql_statement, books)
            connection.commit()
            logger.debug(f"Replaced books: rows={len(books)}")
        except sqlite3.Error:
            connection.rollback()
            raise
        finally:
            connection.close()
```

Append this inside the existing `check_storage.py` at the end of `main()`:

```python
    try:
        storage.replace_books([("New Book", 20.0), (None, 10.0)])
    except sqlite3.IntegrityError:
        print("Replacement failed; original books kept.")
```

Run `python check_storage.py`. We should get:

```text
Replacement failed; original books kept.
```

---

# Part 2: Retrieve One Book Through the API

Connect a GET endpoint to the existing `BookStorage.get_book()` method.

Create `main.py` in the `class16_18`, and copy and paste the following code:

```python
import logging

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from check_storage import BookStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class BookInput(BaseModel):
    title: str
    price: float = Field(ge=0)


class BookResponse(BookInput):
    id: int


app = FastAPI(title="Books Database API")
storage = BookStorage()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = storage.get_book(book_id)
    if book is None:
        logger.warning(f"Book not found: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Retrieved book: id={book_id}")
    return book
```


## Initialize the Table When Storage Starts

Replace `BookStorage.__init__()` in `check_storage.py` with:

```python
    def __init__(self, db_path="data/books.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                price REAL NOT NULL
            )
            """
            connection.execute(sql_statement)
            connection.commit()
            logger.debug(f"Database ready: {self.db_path}")
        finally:
            connection.close()
```


Run from `class-exercise/class16_18/`:

```bash
python -m uvicorn main:app --reload
```


In `http://127.0.0.1:8000/docs`, execute `GET /books/{book_id}`. If you have not run the Class 16 exercise, run `python check_storage.py` once to create the sample books before starting Uvicorn.

---

# Part 3: Test Database Behavior Together

We can test adding and retrieving records, handling invalid inputs, keeping data after a restart, and undoing failed database changes. Today, we will test two of these behaviors: **persistence** and **transaction rollback**.

**Persistence** means that data remains stored even after the program stops. With SQLite, books are saved in a database file, so restarting the API does not erase them.

For example, we should be able to retrieve the same book after restarting the API.

## Test Persistence with a Temporary Database

Create `test_api.py`. 

```python
import sqlite3

import pytest
from fastapi.testclient import TestClient

import main
from check_storage import BookStorage

#The `storage` fixture gives each test a separate temporary database
@pytest.fixture
def storage(tmp_path):
    return BookStorage(tmp_path / "books.db")

#The `client` fixture shows how to connect temporary storage to API tests
@pytest.fixture
def client(storage, monkeypatch):
    #`monkeypatch` makes the API use that test's storage object and restores the original afterward
    monkeypatch.setattr(main, "storage", storage)
    with TestClient(main.app) as test_client:
        yield test_client

def test_storage_persists(storage):
    book_id = storage.add_book("Book A", 12.5)
    reopened = BookStorage(storage.db_path)
    book = reopened.get_book(book_id)
    assert book["title"] == "Book A"
    assert book["price"] == 12.5
```

## Test Transaction Rollback

Add this test to the same `test_api.py`:

```python
def test_failed_replacement_rolls_back(storage):
    storage.add_book("Book A", 12.5)
    storage.add_book("Book B", 25.0)
    before = storage.list_books()

    with pytest.raises(sqlite3.IntegrityError):
        storage.replace_books([("New Book", 20.0), (None, 10.0)])

    reopened = BookStorage(storage.db_path)
    assert reopened.list_books() == before
```

Run both tests:

```bash
python -m pytest test_api.py -v
```

Expect `2 passed`.


---

# Try It Yourself — Add, List, and Search Books

## 1. Add Two Endpoints

```python
@app.post("/books", response_model=BookResponse)
def add_book(book: BookInput):
    # TODO: use storage.add_book(), log the new ID at INFO,
    # and return the stored record with storage.get_book().
    pass


@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
):
    # TODO: pass min_price and limit to storage.list_books().
    # Log the returned row count at INFO and return the list.
    pass
```

The list endpoint should use the storage method's existing filter and sort order. No matches should return `[]` with `200`.

## 2. Add Price-Range Search

Add a new storage method and connect it to an endpoint. For example, `GET /search/books?min_price=10&max_price=20` should return books priced from 10 through 20, including both boundaries.

### Add the Storage Method

Add inside `BookStorage` in `check_storage.py`:

```python
    def search_books(self, min_price, max_price):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            # TODO: SELECT * from books.
            # Use WHERE to filter prices within a specific range. You can use AND to combine the two conditions.
            # Use ORDER BY to sort by price descending, then by ID ascending.
            # Fetch all matching rows and return a list of dictionaries.
            # Log the returned row count at DEBUG.
            pass
        finally:
            connection.close()
```

`AND` requires both price conditions to be true. Return `[]` if no books match.

### Add the Endpoint

Add this endpoint to `main.py`:

```python
@app.get("/search/books", response_model=list[BookResponse])
def search_books(
    min_price: float = Query(ge=0),
    max_price: float = Query(ge=0)
):
    # TODO: if min_price > max_price, log WARNING and raise HTTPException
    # with status 400 and detail (e.g., "min_price must not exceed max_price").
    # Otherwise, call storage.search_books().
    # Log the returned row count at INFO and return the list.
    pass
```

Both parameters are required. Negative prices are rejected with `422`; a reversed range should return `400`.

### Check in `/docs`

1. POST three books priced at `10.0`, `15.0`, and `20.0`.
2. Search with `min_price=10` and `max_price=20`: all three should appear, highest price first. Earlier books in that range may also appear.
3. Search with `min_price=15` and `max_price=15`: only books priced exactly `15.0` should appear.
4. Choose a range above all stored prices: expect `200` and `[]`.
5. Search with `min_price=20` and `max_price=10`: expect `400`.

## After Completing the Exercise

From `class-exercise/class16_18/`:

```bash
cd ..
git status
git add class16_18 requirements.txt
git commit -m "Connect Class 17 SQLite storage to an API and tests"
git push
```

---