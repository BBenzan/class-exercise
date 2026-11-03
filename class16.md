# Weekly Announcements
* **MP3** is posted on Canvas under **Assignments**.
    * MP3-Part 1 is available. 
* **MP3-WSU 1** is due on Friday (11/6) and will be available the night before.
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 

---

# Class 16: SQL and SQLite Fundamentals

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain the difference between SQL, SQLite, a database, and a table.
2. Insert, retrieve, filter, sort, update, and delete records using SQL.
3. Use parameterized queries and manage database connections.
4. Write reusable database methods in a Python class.

---

# Part 0: SQL terminologies (quiz)

SQL is the language we use to work with relational databases. SQLite is a database engine that stores a database in a local file. Python's `sqlite3` module lets Python execute SQL statements.

| Term | Meaning |
| --- | --- |
| Database | A collection of stored tables |
| Table | Rows and named columns for one kind of record. |
| Schema | The table definitions, including columns and constraints. |
| Query | A request to the database, such as selecting matching rows. |

Why use a database?
- As the amount of data grows, a database lets our API retrieve, update, or delete specific records without reading and rewriting an entire data file (e.g. data.csv). 

## Set Up the Exercise

1. Add `class16_18/data/` to the `.gitignore` in `class-exercise/`. Generated database files should not be committed.

2. Create `class16_18/` inside `class-exercise` and go to that directory.

`sqlite3` is included in standard Python installations -- no new pip package or database server is needed.

---

# Part 1: Create the Database and Table (quiz)

Create `check_storage.py` in `class16_18/`. Keep all code in this file. Start with:

```python
import logging
import sqlite3
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    path = Path("data") / "books.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    connection.close()

if __name__ == "__main__":
    main()
```

Run from `class-exercise/class16_18/`:

```bash
python check_storage.py
```

`sqlite3.connect()` opens or creates `books.db`; `sqlite3.Row` allows access by column name.

Inside `main()`, add the following before `connection.close()`. Keep that closing line at the end of the SQL examples throughout Parts 1–4.

```python
    sql_statement = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL
    )
    """

    connection.execute(sql_statement)
    connection.execute("DELETE FROM books")
    connection.commit()
```

`sql_statement` is a Python string containing the SQL command.

* `IF NOT EXISTS` creates a table only when needed.
* `INTEGER`, `TEXT`, and `REAL` specify column types.
* `PRIMARY KEY` identifies a row; SQLite assigns its integer ID on insertion.
* `NOT NULL` requires a value

## `NULL` vs. `NOT NULL`

`NULL` represents a missing value. A column allows `NULL` unless a constraint such as `NOT NULL` prevents it.

| Column definition | Allows missing value? |
| --- | --- |
| `price REAL` | Yes |
| `price REAL NOT NULL` | No |

Python's `None` is stored as SQL `NULL`.

```python
connection.execute(
    "INSERT INTO books (title, price) VALUES (?, ?)",
    ("Book without a price", None)
)
```

---

# Part 2: Insert and Save

Add inside `main()`, before `connection.close()`:

```python
    sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
    cursor = connection.execute(sql_statement, ("Book A", 12.5))
    book_id = cursor.lastrowid
    connection.commit()
```

* Use `?` placeholders so input values are treated as data, preventing quoting errors and SQL injection. Pass values as a tuple or list.
* `execute()` runs SQL and returns a cursor with results or operation information.
* `lastrowid` gives the new book's ID for later retrieval, updates, or deletion.
* `commit()` saves changes.

Add two more books using the same INSERT string:

```python
    connection.execute(sql_statement, ("Book B", 25.0))
    connection.execute(sql_statement, ("Book C", 18.0))
    connection.commit()
```

## Insert Multiple Rows with `executemany()`

Add two more books using executemany():

```python
    rows = [("Book D", 15.0), ("Book E", 10.0)]
    connection.executemany(sql_statement, rows)
    connection.commit()
```

`executemany()` runs the same SQL statement for each tuple in `rows`.

---

# Part 3: Retrieve, Filter, and Limit

Continue inside `main()`, before the closing line.

## Retrieve One Book

```python
    # Retrieve one book 
    sql_statement = "SELECT id, title, price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(dict(row))
```

`fetchone()` returns one row or `None`. `(book_id,)` is a one-item tuple. Use `dict(row)` to print or return the entire row as a dictionary; use `row["price"]` for a single value.

## Preview Rows

```python
    # Preview the first n
    sql_statement = "SELECT * FROM books ORDER BY id LIMIT ?"
    rows = connection.execute(sql_statement, (5,)).fetchall()
    print([dict(row) for row in rows])
```

`*` selects all columns; `fetchall()` returns the result rows as a list. `LIMIT` returns up to the requested number. Change `(5,)` to `(2,)` to preview two rows.

## Filter and Sort

```python
    # Filter and Sort
    sql_statement = """
    SELECT title, price FROM books
    WHERE price >= ? ORDER BY price DESC LIMIT ?
    """
    rows = connection.execute(sql_statement, (15, 2)).fetchall()
    print([dict(row) for row in rows])
```

`WHERE` filters rows; `DESC` sorts highest first (`ASC` sorts lowest first). This query returns Book B followed by Book C. Use `ORDER BY` when result order matters.

---

# Part 4: Count, Update, and Delete

Add each snippet inside `main()`, before `connection.close()`.

## Count

```python
    #Total count
    sql_statement = "SELECT COUNT(*) AS total FROM books"
    row = connection.execute(sql_statement).fetchone()
    print(row["total"])
```

`COUNT(*)` counts rows; `AS total` names the result.

## Update and Check

```python
    #Update
    sql_statement = "UPDATE books SET price = ? WHERE id = ?"
    connection.execute(sql_statement, (13.0, book_id))
    connection.commit()

    #Check
    sql_statement = "SELECT price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(row["price"])  # 13.0
```

## Delete and Check

```python
    #Delete
    sql_statement = "DELETE FROM books WHERE id = ?"
    connection.execute(sql_statement, (book_id,))
    connection.commit()
```

```python
    #Check
    sql_statement = "SELECT * FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(row)  # None
```

---

# Try It Yourself — Reuse SQL with Class Methods

## 1. Complete the Storage Methods

Add this class before `main()` in the same `check_storage.py`. Complete `add_book()`, `get_book()`, and `list_books()` using the SQL examples above.

```python
class BookStorage:
    def __init__(self, db_path="data/books.db"):
        self.db_path = db_path

    def add_book(self, title, price):
        connection = sqlite3.connect(self.db_path)
        try:
            # TODO: INSERT using sql_statement and placeholders.
            # Keep cursor.lastrowid, commit, and log the new ID at DEBUG.
            # Return the assigned ID.
            pass
        except sqlite3.Error:
            #For a failed write, `rollback()` cancels uncommitted changes and `raise` passes the error to the caller.
            connection.rollback()
            raise
        finally:
            # Always close the connection, whether the operation succeeds or fails.
            connection.close()

    def get_book(self, book_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            # TODO: SELECT by ID using a placeholder and fetchone().
            # Log the ID and whether a row was found (e.g., not None) at DEBUG.
            # Return None if missing; otherwise, return dict(row).
            pass
        finally:
            connection.close()

    def list_books(self, min_price=0, limit=100):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            # TODO: SELECT id, title, and price where price >= min_price.
            # Sort price DESC, then id ASC (comma-separated), 
            # and Apply limit.
            # Use placeholders and fetchall(); return a list of dictionaries.
            # Log the returned row count at DEBUG.
            pass
        finally:
            connection.close()
```

Each method opens and closes its own connection. For a failed write, `rollback()` cancels uncommitted changes and `raise` passes the error to the caller.

Append these calls inside the existing `main()`, __after__ `connection.close()` (keep all earlier code):

```python
    # ...
    # connection.close()

    storage = BookStorage()
    book_id = storage.add_book("Book A", 12.5)
    logger.info(f"Added book: id={book_id}")
```


## 2. Check the Result

Append to the existing `main()`, after the `add_book()` call and its log:

```python
    print(storage.get_book(book_id)["title"])
    print(storage.get_book(book_id)["price"])
    books = storage.list_books(min_price=15, limit=2)
    print([(book["title"], book["price"]) for book in books])
```

Run:

```bash
python check_storage.py
```

After the earlier SQL output, the final three lines should be:

```text
Book A
12.5
[('Book B', 25.0), ('Book C', 18.0)]
```

Try changing `min_price` to `100` to check an empty result.

## After Completing the Exercise

From `class-exercise/`:

```bash
cd ..
git status
git add .gitignore class16_18
git commit -m "Add Class 16 SQLite storage and SQL queries"
git push
```
