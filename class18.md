# Weekly Announcements

* **MP3** is posted on Canvas under **Assignments**.
    * MP3-Parts 1 and 2 are available. 
* **MP3-WSU 2** is due on Friday (11/13) and will be available the night before.
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 
* **MP3 Push Day (Friday 11/13)**
    - We don't meet in class
    - Links will be posted in a Canvas announcement

---

# Class 18: Caching with fakeredis

Today, you will review completed code on your own to understand how caching works. Add the provided code to your Class 17 project, follow the explanations, and run it as you go. In Try It Yourself, you will connect cache invalidation to the POST endpoint and complete a test.

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain cache hits, cache misses, and expiration.
2. Cache a database query result using `fakeredis`.
3. Choose keys that distinguish requests with different parameters.
4. Invalidate cached results after successfully adding a book.
5. Test that cache hits skip database queries and successful writes invalidate cached results.

> Continue inside `class-exercise/class16_18/` using your completed Class 17 code and the same virtual environment.

---

# Setup

```bash
# in class-exercise
python -m pip install fakeredis
python -m pip freeze > requirements.txt
```

After setup, go to `class-exercise/class16_18/`

---

# Part 0: Why Cache? (quiz)

Repeated GET requests with the same parameters run the same SQL query. A **cache** stores a temporary copy of the result so we can reuse it and avoid repeating the same database query.

| Situation | Action |
| --- | --- |
| Cache hit | Return the cached result. |
| Cache miss | Query SQLite, cache the result, and return it. |
| Successful write | Invalidate cached results so the next request reads SQLite. |

Use `fakeredis` to practice this behavior locally.

| Existing endpoint | New behavior |
| --- | --- |
| `GET /books` | Cache the list response using `min_price` and `limit`. |
| `GET /books/{book_id}` | Keep the single-book lookup unchanged and uncached. |
| `GET /search/books` | Keep price-range search unchanged and uncached. |
| `POST /books` | Save the book, then invalidate cached list responses. |

---

# Part 1: Store and Retrieve Cached Results (quiz)

## 1. Add Imports

Add to `main.py`:

```python
import json
import fakeredis
```

## 2. Add the Complete Cache Class

Add `BookCache` immediately below `BookResponse` in `main.py`, before `app = FastAPI(...)`:

```python
class BookCache:
    def __init__(self):
        self.client = fakeredis.FakeRedis(decode_responses=True)

    def make_key(self, min_price, limit):
        return f"books:min_price:{float(min_price)}:limit:{limit}"

    def get(self, min_price, limit):
        key = self.make_key(min_price, limit)
        value = self.client.get(key)
        if value is None:
            logger.debug(f"Cache MISS: {key}")
            return None
        logger.debug(f"Cache HIT: {key}")
        return json.loads(value)

    def set(self, min_price, limit, books):
        key = self.make_key(min_price, limit)
        self.client.set(key, json.dumps(books), ex=60)
        logger.debug(f"Cached result: {key}")

    def invalidate(self):
        self.client.flushdb()
        logger.debug("Invalidated book query cache")
```

## Let's Review the Code

* **`__init__()`** creates the cache. `decode_responses=True` returns strings rather than bytes.
* **`make_key()`** includes both `min_price` and `limit` because different parameters may return different books. `float(min_price)` gives `0` and `0.0` the same key.
* **`get()`** checks the key and logs HIT or MISS. The cache client's `get(key)` returns the stored value, or `None` if the key is missing or expired—similar to Python's `dict.get()`. `json.loads()` converts a stored JSON string back to a Python list.
* **`set()`** uses `json.dumps()` to convert the book list to JSON, then stores it with `ex=60`. This expiration period is its TTL (time to live).
* **`invalidate()`** calls `flushdb()` to clear all entries in this dedicated cache and logs the invalidation. In TIY, we will call it after successfully saving a new book.

## 3. Create the Cache Object

Below the existing `storage` object, add:

```python
cache = BookCache()
```

---

# Part 2: Extend the Same GET Endpoint

## Add the Complete Endpoint

Replace the existing `GET /books` function in `main.py` with the completed version below. It adds cache lookup and storage around the existing SQL retrieval.

```python
@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
):
    cached = cache.get(min_price, limit)
    if cached is not None:
        logger.info(f"Listed books: rows={len(cached)}")
        return cached
    books = storage.list_books(min_price, limit)
    cache.set(min_price, limit, books)
    logger.info(f"Listed books: rows={len(books)}")
    return books
```

## Let's Review the Code

1. **Look up the cache:** `cache.get(min_price, limit)` checks for a response to the same request parameters.
2. **Cache hit:** log the row count and return immediately, skipping SQLite.
3. **Cache miss:** call the existing `storage.list_books()` method, cache its result, and return it.

A cached `[]` is a valid result, so use `cached is not None` rather than `if cached`.

## Run and Check

Start Uvicorn:

```bash
python -m uvicorn main:app --reload
```

In `http://127.0.0.1:8000/docs`, send the same GET requests __twice__ 


Expect `Cache MISS`, then `Cache HIT` in the terminal. Expired entries produce another miss.

---

# Part 3: Invalidate After Changes

## Add the Complete Client Fixture

In `test_api.py`, keep the storage fixture and both Class 17 tests: `test_storage_persists()` and `test_failed_replacement_rolls_back()`. Replace only the client fixture with:

```python
@pytest.fixture
def client(storage, monkeypatch):
    monkeypatch.setattr(main, "storage", storage)
    monkeypatch.setattr(main, "cache", main.BookCache())
    with TestClient(main.app) as test_client:
        yield test_client
```

## Let's Review the Code

* The first `monkeypatch.setattr()` makes API requests use the test's temporary database.
* The second makes them use a fresh `BookCache`, so cache entries do not carry over between tests.
* `TestClient` sends requests to the app without running Uvicorn. `monkeypatch` restores the original objects after the test.

A database write does not update a separate cached copy. A new book may affect filtered or limited results, so we will call `cache.invalidate()` after a successful POST in TIY. TTL eventually removes old entries; invalidation clears them immediately.

The existing persistence and rollback tests remain unchanged. Run them to confirm `2 passed`:

```bash
python -m pytest test_api.py -v
```

---

# Part 4: Verify a Cache Hit Together

## Add the Complete Cache-Hit Test

Add this test to `test_api.py`:

```python
def test_cache_hit_skips_database(client, monkeypatch):
    response = client.post("/books", json={"title": "Book A", "price": 12.5})
    assert response.status_code == 200

    first = client.get("/books", params={"min_price": 0, "limit": 100})
    assert first.status_code == 200

    def fail_if_called(*args, **kwargs):
        pytest.fail("A cache hit should not query the database")

    monkeypatch.setattr(main.storage, "list_books", fail_if_called)

    second = client.get("/books", params={"min_price": 0, "limit": 100})
    assert second.status_code == 200
    assert second.json() == first.json()
```

## Let's Review the Code

1. **POST a book** to the test database.
2. **Send the first GET** to fill the cache and keep its response.
3. **Replace `storage.list_books()`** using `monkeypatch.setattr()`. Its temporary replacement, `fail_if_called()`, makes the test fail whenever it is called. `*args` and `**kwargs` let it accept any arguments passed to the original method.
4. **Repeat the same GET.** If it queries SQLite instead of using the cache, it calls `fail_if_called()` and the test fails. A cache hit skips that method and returns the same response.

## Run and Check

```bash
python -m pytest test_api.py -v
```

Expect `3 passed`: the two Class 17 storage tests and the new cache-hit test.

---

# Try It Yourself — Connect Cache Invalidation

## 1. Update the Existing POST Endpoint

In `main.py`, find the `add_book()` function for `POST /books`. Add `cache.invalidate()` directly after the line that saves the book:

```python
book_id = storage.add_book(book.title, book.price)
cache.invalidate() # Add this line
```
This clears cached lists so the next GET retrieves the updated data from SQLite.

## 2. Add One Test

Add to the `test_api.py`:

```python
def test_add_book_invalidates_cache(client):
    response = client.post("/books", json={"title": "Book A", "price": 12.5})
    assert response.status_code == 200
    # TODO 1: Send two GET requests with min_price=0:
    # one with limit=1 and another with limit=100.
    # Assert 200 and check both entries using main.cache.get(0, limit).
    # TODO 2: repeat limit=100 and check the same response.
    # TODO 3: POST Book B at 20.0; assert 200 and both old entries are None.
    # TODO 4: GET again with limit=100; check both books,
    # their price-descending order, and the cached response.
    pass
```

```bash
python -m pytest test_api.py -v
```

Expect `4 passed`: persistence, rollback, cache hit, and invalidation. Inspect cache contents directly; no log-capture fixture is required.

## 3. Run and Check

In `http://127.0.0.1:8000/docs`, 
- Use `POST /books` to add `Book A` with a price of `10`.
- Call `GET /books` with min_price=0 and limit=100. Check the server logs: cache miss.
- Repeat the same GET request. Check the logs: cache hit.
- Call GET with min_price=0 and limit=1. This uses a different cache key: cache miss.
- Use `POST /books` to add `Book B` with a price of `20`. This should clear both cached results.
- Call GET with min_price=0 and limit=100 again. Check for a cache miss and confirm that Book B appears in the response.
- Repeat the same GET request once more. Check the logs: cache hit.

After a server restart, books remain in SQLite while the cache starts empty. 


For example:

```text
10:15:02 DEBUG    main — Cache MISS: books:min_price:0.0:limit:100
10:15:03 DEBUG    main — Cache HIT: books:min_price:0.0:limit:100
10:15:04 DEBUG    main — Cache MISS: books:min_price:0.0:limit:1
10:15:05 DEBUG    main — Invalidated book query cache
10:15:06 DEBUG    main — Cache MISS: books:min_price:0.0:limit:100
10:15:07 DEBUG    main — Cache HIT: books:min_price:0.0:limit:100
```

To check expiration, wait more than 60 seconds after a cache miss, then repeat the same GET: expect another miss. Avoid adding books or restarting the server during this check. A cache hit does not reset the TTL.

## After Completing the Exercise

From `class-exercise/class16_18/`:

```bash
cd ..
git status
git add class16_18 requirements.txt
git commit -m "Add Class 18 query caching and invalidation tests"
git push
```

---