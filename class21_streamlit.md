# Weekly Announcements

* Final Project team formation survey is due today (11/20) 11:59 ET.

---

# Class 21: Build a Streamlit Client

## Learning Objectives

By the end of today's class, you will be able to:

1. Create and run a Streamlit application.
2. Send HTTP requests to your existing API using `requests`.
3. Connect user inputs to tables and charts.
4. Display useful messages for empty results and request failures.

---

# Part 0: From `/docs` to Our Own Interface

Streamlit is a Python library for building interactive web applications. You can add inputs, tables, and charts using Python.

So far, we've used FastAPI’s /docs page to send requests and inspect responses. Today, we will build our own interface with Streamlit: users choose inputs, Streamlit sends requests to FastAPI, and the results appear as tables and charts.

In our application, Streamlit handles user interaction and displays results, while FastAPI receives requests, processes data, and returns results. The two applications communicate through HTTP requests and responses.


```bash
# in the class-exercise, after starting venv
python -m pip install streamlit requests
python -m pip freeze > requirements.txt
```

---

# Part 1: Start with a Simple Page

Create `streamlit_app.py`:

```python
import streamlit as st

st.title("Movie Explorer")
st.write("Explore genre summaries and yearly rating trends.")

min_movies = st.slider("Minimum movies per genre", 1, 6, 3)
st.write("Selected minimum:", min_movies)
```

Run:

```bash
python -m streamlit run streamlit_app.py
```

Open the local URL printed in the terminal, normally `http://localhost:8501`. Move the slider and observe the displayed value.

The slider arguments above set the label, minimum, maximum, and default value. By default, changing a widget reruns the script from top to bottom with the new value. We do not need a loop to update the page.

---

# Part 2: Request Data from the API (quiz)

**Question:** How can the interface request only genres with at least three movies?

In a second terminal, activate the same environment and go to `class-exercise/class20_21/`. Start the existing API:

```bash
python -m uvicorn main:app --reload
```

Keep both processes running:

| Process | Command | Default address |
| --- | --- | --- |
| FastAPI server | `python -m uvicorn main:app --reload` | `http://127.0.0.1:8000` |
| Streamlit application | `python -m streamlit run streamlit_app.py` | `http://localhost:8501` |

Create `api_client.py`:

```python
import logging

import requests

logger = logging.getLogger(__name__)
API_URL = "http://127.0.0.1:8000"


def fetch_records(endpoint, params=None):
    response = requests.get(
        f"{API_URL}{endpoint}", params=params, timeout=10
    )
    response.raise_for_status()
    records = response.json()
    logger.debug(f"Fetched {endpoint}: rows={len(records)}")
    return records

```

* `requests.get()` makes an actual HTTP request to the running API.
* `params` supplies query parameters, such as `min_movies=3`.
* `raise_for_status()` raises an HTTP error for a 4xx or 5xx response.
* `response.json()` converts the JSON response into Python data: here, a list of dictionaries.
* `timeout=10` sets a timeout for connection and response-read waits.

Unlike TestClient, `requests` needs the API server to be running. This request code runs in the Streamlit Python process, so no browser CORS setup is needed for this example.

## Calling a POST Endpoint

We used `requests.get()` here, but you can also use `requests.post()` to call a POST endpoint. Use `json=` to send a JSON request body.

For example, with the Class 17 book API running, this request adds a book:

```python
response = requests.post(
    "http://127.0.0.1:8000/books",
    json={"title": "Book A", "price": 10.0},
    timeout=10,
)
response.raise_for_status()
result = response.json()
```

This is a separate example; today's movie analysis API does not have a `POST /books` endpoint.


---

# Part 3: Show the Answer as a Table and Chart

Replace the simple page in `streamlit_app.py` with:

```python
import logging

import pandas as pd
import requests
import streamlit as st

from api_client import fetch_records

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

st.title("Movie Explorer")
st.write("Explore genre summaries and yearly rating trends.")

st.header("Which genres have the highest average ratings?")
min_movies = st.slider("Minimum movies per genre", 1, 6, 3)

try:
    records = fetch_records("/analysis/genres", {"min_movies": min_movies})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve genre summary: {error}")
    st.error("Cannot load genre data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No genres match this minimum movie count.")
else:
    genre_df = pd.DataFrame(records)
    st.dataframe(genre_df, hide_index=True)
    st.bar_chart(genre_df, x="genre", y="average_rating")
    logger.info(f"Displayed genre summary: groups={len(genre_df)}")
```

Save the file and rerun the Streamlit page if prompted. The API returns grouped results; Streamlit converts them into a DataFrame for display without recalculating the analysis.

`st.dataframe()` displays a table, and `st.bar_chart()` uses `genre` and `average_rating` for its axes. `st.error()` displays an error; `st.stop()` stops the current script run so the page does not continue with missing data.

## Try the Same Question with Different Inputs

1. Set the minimum to `1`: four genres appear, including Documentary.
2. Set it to `3`: Comedy, Drama, and Action remain; Documentary is excluded.
3. Set it to `6`: the page shows the empty-result message instead of a chart.

With `min_movies=3`, the table should contain:

| genre | movie_count | average_rating |
| --- | ---: | ---: |
| Comedy | 3 | 8.00 |
| Drama | 5 | 7.80 |
| Action | 3 | 7.67 |

Formatting and chart category order may differ. Watch the API terminal: changing the slider sends a new GET request. Application logs appear in their corresponding terminals.

---

# Part 4: Visualization Examples with Streamlit

Streamlit can draw charts directly from a DataFrame. Try these examples in a separate file, `chart_examples.py`, so you can explore the chart syntax before using it in the movie app.

```python
import pandas as pd
import streamlit as st

st.title("Streamlit Chart Examples")

# Each row represents one year.
example_df = pd.DataFrame({
    "year": [2020, 2021, 2022, 2023],
    "average_rating": [7.0, 8.0, 8.0, 9.0],
    "rolling_rating": [7.0, 7.5, 7.67, 8.33],
    "movie_count": [2, 4, 3, 6],
})

st.dataframe(example_df, hide_index=True)

st.header("Bar chart: compare values")
st.bar_chart(example_df, x="year", y="movie_count")

st.header("Line chart: show a trend")
st.line_chart(example_df, x="year", y="average_rating")

st.header("Two lines: compare trends")
st.line_chart(
    example_df,
    x="year",
    y=["average_rating", "rolling_rating"],
)

st.header("Scatter plot: explore a relationship")
st.scatter_chart(example_df, x="movie_count", y="average_rating")
```

Run this file instead of the movie interface while trying the examples. You can stop the current Streamlit process with `Ctrl+C` first:

```bash
python -m streamlit run chart_examples.py
```

## Let's Review

| Call | Use |
| --- | --- |
| `st.dataframe()` | Display the underlying data as a table. |
| `st.bar_chart()` | Compare values across categories or observations. |
| `st.line_chart()` | Show changes over an ordered axis, such as time. |
| `st.scatter_chart()` | Explore the relationship between two numeric columns. |

* The first argument is the DataFrame containing the data.
* `x` names the column for the horizontal axis.
* `y` names the column for the vertical axis. For the line chart, passing a list of two column names draws two lines.
* Each scatter point above represents one year, with its movie count and average rating.
* `st.dataframe()` is a table display; the chart calls visualize selected columns from that same data.

These examples use prepared data to practice display syntax. In the movie application, the API calculates the results and Streamlit displays them.

Before continuing with TIY, stop the chart example with `Ctrl+C` and restart the movie interface:

```bash
python -m streamlit run streamlit_app.py

```

Keep the FastAPI server running in the other terminal.

---

# Part 5: Let's Add the Yearly Trend

Continue in the same `streamlit_app.py`. Keep the completed genre section and reuse `fetch_records()`.

## 1. Add a Window Input

Append below the genre section:

```python
st.header("How have ratings changed over time?")
window = st.slider("Rolling window (yearly observations)", 1, 6, 3)

# TODO: Request /analysis/years with window as a query parameter.
# Catch requests.RequestException and show an error, then call st.stop().
# If the returned list is empty, show an informational message.
# Otherwise, create a DataFrame and display its table.
# Show a line chart with release_year on the x-axis and
# average_rating and rolling_rating as the two lines.
# Log the year count and selected window at INFO.
```


## 2. Run and Check

Keep both servers running and check:

1. `window=3`: the year table has six rows; 2024's rolling rating is `8.67`.
2. `window=1`: the two lines overlap because the rolling values equal the yearly averages.
3. Set `min_movies=6`: the empty genre message appears, while the yearly section still works.
4. Stop Uvicorn, then change a slider: show the error message without a Python traceback on the page.
5. Restart Uvicorn and change a slider: the page loads the results again.

Expected yearly values for `window=3`:

| release_year | average_rating | rolling_rating |
| --- | ---: | ---: |
| 2019 | 7.0 | 7.00 |
| 2020 | 7.0 | 7.00 |
| 2021 | 8.0 | 7.33 |
| 2022 | 8.0 | 7.67 |
| 2023 | 9.0 | 8.33 |
| 2024 | 9.0 | 8.67 |

Example Streamlit application logs:

```text
10:15:02 DEBUG    api_client — Fetched /analysis/genres: rows=3
10:15:02 INFO     __main__ — Displayed genre summary: groups=3
10:15:02 DEBUG    api_client — Fetched /analysis/years: rows=6
10:15:02 INFO     __main__ — Displayed yearly trend: years=6, window=3
```

---

# Try It Yourself — Build One Feature from Function to Interface

**This exercise is practice for your final project.** Implement a new feature through all three layers: a Python function, an API endpoint, and a Streamlit interface. Use the same pattern when building your team's own features.

**Feature:** let the user choose a minimum rating and view movies whose ratings meet that minimum.

## 1. Add the Function

In `check_analysis.py`, add this function before `main()`. Keep the existing summary functions:

```python
def filter_movies(df, min_rating):
    # TODO: Keep rows where rating >= min_rating.
    # Return a DataFrame containing title, release_year, rating, and genre.
    # Preserve the original row order.
    pass
```

## 2. Connect It to FastAPI

In `main.py`, add `filter_movies` to the import from `check_analysis`. Keep the existing endpoints and add:

```python
@app.get("/movies/filter", response_model=list[dict])
def get_filtered_movies(min_rating: float = Query(default=8.0, ge=0, le=10)):
    # TODO: Call filter_movies() with df and min_rating.
    # Log the returned row count at INFO and return records.
    pass
```

Check the endpoint in `http://127.0.0.1:8000/docs` before connecting the interface. A minimum of `0` should return every movie; a minimum above `10` should return `422`.

## 3. Connect It to Streamlit

Append a new section after the yearly trend in `streamlit_app.py`:

```python
st.header("Which movies meet your minimum rating?")
min_rating = st.slider("Minimum movie rating", 0.0, 10.0, 8.0, 0.5)

# TODO: Use fetch_records() to request /movies/filter with min_rating.
# Catch requests.RequestException, show an error, and call st.stop().
# If the list is empty, show an informational message.
# Otherwise, display the returned records as a DataFrame table.
# Log the displayed row count and minimum rating at INFO.
```

Reuse `api_client.py` unchanged. Filtering belongs in the API-side function; Streamlit sends the input and displays the returned records.

## 4. Run and Check the Complete Feature

1. Set the minimum rating to `0`: the table contains all 12 movies.
2. Set it to `8.0`: every returned movie has a rating of at least `8.0`.
3. Set it to `10.0`: only the Documentary movie remains.
4. Watch the API terminal when you move the slider: the page sends a request containing the selected `min_rating`.
5. Explain the path from the slider value to the function and back to the displayed table.

The sample contains a movie rated `10`, so this slider does not produce an empty result with the supplied data. Still include the empty-result branch so the feature handles other datasets.

---

## After Completing the Exercise

From `class-exercise/class20_21/`:

```bash
cd ..
git status
git add class20_21 requirements.txt
git commit -m "Add Streamlit client for the movie analysis API"
git push
```

---
