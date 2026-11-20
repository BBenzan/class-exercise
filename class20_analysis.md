# Weekly Announcements

* **Final Project Overview** is available on Canvas > Files
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    - Strongly recommended if you need help with your assignment or quiz preparation. 
---

# Class 20: From Questions to Analysis Results

## Learning Objectives

By the end of today's class, you will be able to:

1. Turn a data question into grouped summaries.
2. Combine multiple aggregations and filter their results.
3. Calculate and interpret a rolling average.
4. Return analysis results through an API.

---

# Part 0: Project Overview

The project overview is available on Canvas. Make sure to review it!

First deadline is due this Friday (11/20).

---

# Part 1: Which Genre Has the Highest Average Rating? (quiz)

- Create `class20_21/` inside `class-exercise` and go to that directory. 

- Create `data/` and save the provided `class20_movies.csv` there. 

- Add `class20_21/data/` to your `.gitignore`. 

- Create `check_analysis.py`:

```python
from pathlib import Path

import pandas as pd


def main():
    df = pd.read_csv(Path("data") / "class20_movies.csv")
    print(df.groupby("genre")["rating"].mean())


if __name__ == "__main__":
    main()
```

Run:

```bash
python check_analysis.py
```

Expected averages:

| genre | average rating |
| --- | --- |
| Action | 7.67 |
| Comedy | 8.00 |
| Documentary | 10.00 |
| Drama | 7.80 |

`groupby("genre")` groups movies by genre; `mean()` calculates one average per group. 

**Question:** Documentary has the highest average. Is that enough information to recommend it?

---

# Part 2: Does Each Average Have Enough Movies Behind It?

Continue in `check_analysis.py`. Add `summarize_genres()` function below before `main()`:

```python
def summarize_genres(df):
    summary = df.groupby("genre", as_index=False).agg(
        movie_count=("title", "count"),
        average_rating=("rating", "mean"),
    )
    summary = summary.sort_values(
        ["average_rating", "genre"], ascending=[False, True]
    )
    summary["average_rating"] = summary["average_rating"].round(2)
    return summary
```

`agg()` calculates several summaries at once. Each pair names the source column and operation; for example, `movie_count=("title", "count")` counts non-missing titles. `as_index=False` keeps `genre` as a regular column.

In the same file's `main()`, replace the previous print statement with:

```python
    print(summarize_genres(df).to_string(index=False))
```

Expected result:

```text
      genre  movie_count  average_rating
Documentary            1           10.00
     Comedy            3            8.00
      Drama            5            7.80
     Action            3            7.67
```

---

# Part 3: How Does the Average Change Over Time? (quiz)

In `check_analysis.py`, add this function before `main()`:

```python
def summarize_years(df):
    summary = df.groupby("release_year", as_index=False).agg(
        average_rating=("rating", "mean")
    )
    summary = summary.sort_values("release_year")
    summary["rolling_rating"] = summary["average_rating"].rolling(
        window=3, min_periods=1
    ).mean()
    summary[["average_rating", "rolling_rating"]] = summary[
        ["average_rating", "rolling_rating"]
    ].round(2)
    return summary
```

Update `main()` to call both analysis functions:

```python
def main():
    df = pd.read_csv(Path("data") / "class20_movies.csv")
    print(summarize_genres(df).to_string(index=False))
    print(summarize_years(df).to_string(index=False))
```

Run `python check_analysis.py` to see both results.

A rolling average summarizes the current row and preceding rows in the window. Sort by time first. Here, each row is a year's average, so the window includes up to three yearly averages.

| release_year | average_rating | rolling_rating |
| --- | --- | --- |
| 2019 | 7.0 | 7.00 |
| 2020 | 7.0 | 7.00 |
| 2021 | 8.0 | 7.33 |
| 2022 | 8.0 | 7.67 |
| 2023 | 9.0 | 8.33 |
| 2024 | 9.0 | 8.67 |


---

# Part 4: Analysis API

Create `main.py`:

```python
import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query

from check_analysis import summarize_genres

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie Analysis API")
df = pd.read_csv(Path("data") / "class20_movies.csv")


@app.get("/analysis/genres", response_model=list[dict])
def get_genres():
    result = summarize_genres(df)
    logger.info(f"Returned genre summary: groups={len(result)}")
    return result.to_dict(orient="records")
```

Run from `class-exercise/class20_21/`:

```bash
python -m uvicorn main:app --reload
```

In `http://127.0.0.1:8000/docs`, execute `GET /analysis/genres`. Expect `200` and four records containing `genre`, `movie_count`, and `average_rating`.

---

# Try It Yourself — Extend the Same Analysis API

## 1. Filter Small Groups

Update the existing function in `check_analysis.py`:

```python
def summarize_genres(df, min_movies=1):
    summary = df.groupby("genre", as_index=False).agg(
        movie_count=("title", "count"),
        average_rating=("rating", "mean"),
    )
    # TODO: Keep only groups with movie_count >= min_movies.
    summary = summary.sort_values(
        ["average_rating", "genre"], ascending=[False, True]
    )
    summary["average_rating"] = summary["average_rating"].round(2)
    logger.debug(f"Genre summary: groups={len(summary)}")
    return summary
```

Update the existing endpoint:

```python
@app.get("/analysis/genres", response_model=list[dict])
def get_genres(min_movies: int = Query(default=1, ge=1)):
    # TODO: Pass min_movies to summarize_genres().
    # Log the number of groups at INFO and return records.
    pass
```

## 2. Return the Yearly Trend

Update the existing `summarize_years()` in `check_analysis.py` to accept a `window` parameter. Complete the TODO using `window` instead of the fixed value `3` from Part 3:

```python
def summarize_years(df, window=3):
    summary = df.groupby("release_year", as_index=False).agg(
        average_rating=("rating", "mean")
    )
    summary = summary.sort_values("release_year")

    # TODO: Add rolling_rating using window and min_periods=1.

    summary[["average_rating", "rolling_rating"]] = summary[
        ["average_rating", "rolling_rating"]
    ].round(2)
    logger.debug(f"Year summary: years={len(summary)}, window={window}")
    return summary
```

In `main.py`, add `summarize_years` to the import from `check_analysis`, then add this endpoint:

```python
@app.get("/analysis/years", response_model=list[dict])
def get_years(window: int = Query(default=3, ge=1)):
    # TODO: Call summarize_years() with window.
    # Log the year count and window at INFO and return records.
    pass
```

## 3. Run and Check

In `http://127.0.0.1:8000/docs`:

1. GET `/analysis/genres` with `min_movies=3`: three groups, with Comedy first. Documentary is excluded.
2. GET `/analysis/years` with `window=3`: six records; the last rolling value is `8.67`.



## After Completing the Exercise

From `class-exercise/class20_21/`:

```bash
cd ..
git add class20_21 requirements.txt .gitignore
git commit -m "Add grouped movie analysis and rolling averages API"
git push
```

---
