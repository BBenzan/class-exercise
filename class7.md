# Weekly Announcements

* Quiz section in the syllabus has been updated
    * "Quiz Score Interpretation"
* MP1 Check-off Meeting
    * More information will be shared next week
    * TAs will send you an email next week to begin scheduling 
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
* **MP 1** is posted on Canvas under **Assignments**.
    * MP 1 - Parts 1-3 are available. 
* **MP1-WSU 3** is due TODAY (Friday, 10/2).

    

## MP1-WSU 3
If you’re ready and would like to complete it now, feel free to do so. 

---

# Class 7: Outliers, Text Cleaning, and Cleaning Workflows

## Learning Objectives

By the end of today's class, you will be able to:

1. Detect numeric outliers using IQR and z-scores.
2. Clean inconsistent text values.
3. Explain cleaning workflows
    - Apply cleaning steps in an intentional order.
    - Compare a DataFrame before and after cleaning.

> Note: All exercises we do in class are expected to be completed inside the `class-exercise` directory. Please make sure to navigate there (e.g., `cd class-exercise`) before starting any coding practice during class. Also make sure your virtual environment is active before running Python or installing packages.

---

# Part 1: The Reality of Messy Data

Real datasets often contain:

- Duplicate rows
- Missing values
- Extreme numeric values
- Text: Inconsistent format, typo, ...
- ...

Create a sample dataframe:

```python
import pandas as pd
data = {"ID":range(100),"Score":[10]*2+[20]*3+[30]*5+[50]*15+[60]*20+[70]*25+[80]*15 +[90]*8 +[100,100,5,5,0,0,5000]}

df = pd.DataFrame(data)
print(df)
```

> Note: There is no one universal command for cleaning. Each problem requires a decision.

## Inspect Before Cleaning

```python
print(df.shape)
print(df.dtypes)
print(df.describe())
```

Before changing the data, save a copy:

```python
df_original = df.copy()
```

This lets you compare the original and cleaned results later.

---



# Part 2: Numeric Outliers

An outlier is a value that is unusually far from most other values.

Outliers may represent:

- A data-entry error
- A rare but valid observation
- A measurement problem

## Visual Example
```python
import matplotlib.pyplot as plt
df['Score'].plot.hist(bins=300, edgecolor='black')
plt.show()

#Without the last score of 5000. 
df['Score'][:-1].plot.hist(bins=300, edgecolor='black')
plt.show()
```

## IQR Method (quiz)

The interquartile range uses the middle 50% of the data.

```text
IQR = Q3 - Q1

lower bound = Q1 - 1.5 × IQR
upper bound = Q3 + 1.5 × IQR
```

Calculate the bounds:

```python
q1 = df["Score"].quantile(0.25)
q3 = df["Score"].quantile(0.75)
iqr = q3 - q1

# Use the equation above to replace None
lower = None
upper = None

print(lower)
print(upper)
```

Keep rows inside the bounds:

```python
df_score_cleaned = df[(df["Score"] >= lower) & (df["Score"] <= upper)]
```

## Z-Score Method (quiz)

Z-Score measures the number of standard deviations between an individual point and the mean.

```text
z-score(s) = (value(s) - mean) / standard deviation
```

```python
mean = df["Score"].mean()
std = df["Score"].std()

# Use the equation above to replace None
z_scores = None
```

Keep rows within three standard deviations:

```python
df_score_cleaned = df[z_scores.abs() <= 3]
```

## IQR vs. Z-Score

| Method | Useful when |
| :--- | :--- |
| IQR | Data is skewed or not normally distributed |
| Z-score | Data is approximately normally distributed |

The threshold is a decision:

```python
iqr_threshold = 1.5
zscore_threshold = 3
```

>Do not remove an outlier only because it is large. First understand the context.

# Part 3: Text Cleaning

Text values can differ because of capitalization, whitespace, typo.

These values should often represent the same category.


```python
import pandas as pd
data = {"ID":range(4),"Message":["Now Here  "," now here ", "  NOW HERE", "Now   here"]}
df = pd.DataFrame(data)
print(df)
```

## Str Methods for Simple Cleaning 

```python
# Strip Whitespace
df["Message"] = df["Message"].str.strip()
print(df)
# Convert to Lowercase
df["Message"] = df["Message"].str.lower() 
print(df)

# removing repeated whitespace between words?
print(df["Message"].str.replace(' ',''))
```

## Regex for Deep Cleaning 

Regex, short for **regular expression**, is a sequence of characters that defines a pattern for text.

| Pattern | Meaning |
| :--- | :--- |
| `\s` | One whitespace character |
| `\S` | One non-whitespace character |
| `+` | One or more repetitions |
| `?` | Zero or one repetition |
| `*` | Zero or more repetition |

* there are more patterns -- see more examples from https://www.rexegg.com/regex-quickstart.php or other websites.  

Regex patterns are written as raw strings(`r""`):

```python
#Difference between "" vs r""
print("a\nb") #a    b
print(r"a\tb") # a\tb

#One or more consecutive whitespace characters
pattern = r"\s+"

#One or more consecutive non-whitespace characters
pattern = r"\S+"
```

We use a module (e.g., `import re`) to work with regex
- Use `re.sub(pattern, replacement, text)` to replace matching text. 
- Use `re.findall(pattern, text)` to find all matching occurences (in a list). 

```python
import re
re.sub(r"\s+", " ", "Hi     there") 
re.findall(r"\S+", "Hi there") 
```

### Cleaning Repeated Whitespace
```python
import re

def clean_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text
```

Apply it to a column:

```python
df["Message"] = df["Message"].apply(clean_text)
```

For additional text cleaning, consider using `str.replace()` or other regular expressions, such as patterns for URLs.

### URL Cleaning Example

```python
links = ["Visit https://example.com for more info", "My link: www.github.com/mylink/", "Visit http://www.google.com/search"]
data = pd.Series(links)

print(data)

def replace_url(text):
    text = re.sub(r"https?://\S+|www\.\S+", "URL", text)
    return text
# Remove URLs
data = data.apply(replace_url)
print(data)
```


---

# Part 4: Cleaning Order and Reporting 

Things we could do for cleaning:
```
Remove numeric outliers
Clean text columns
Handle missing values
Remove exact duplicates
...
```

The order of operations can change the result.

A reasonable order is:

```text
1. Remove exact duplicates
2. Handle missing values
3. Remove numeric outliers
4. Clean text columns
5. Compare before and after
```

Another project may require a different order, so the order should be intentional.


---

# Try It Yourself — Build a Netflix Pipeline, Continued

Continue using the `class6_7_netflix_utils.py` and `class6_7_netflix_pipeline.py` files that you completed in Class 6. You will add outlier and text-cleaning functions, then extend the existing workflow.

Try it yourself as much as possible, and we will go through the solution together before class ends.

## If you finish early and feel confident about the exercise,

* Get checked off by either me or a TA.
* Once you have been checked off, you may leave.


## Before You Start

Make sure your virtual environment is active:

```bash
# Mac/Linux
source venv/bin/activate     

# Windows
venv\Scripts\activate  
#OR
venv\Scripts\activate.ps1  
```

Open your `class-exercise` folder. Keep `messy_netflix_titles.csv` inside the same `data/` directory used in Class 6.

Make sure the completed Class 6 files are available:

```text
class-exercise/
├── class6_7_netflix_utils.py
├── class6_7_netflix_pipeline.py
└── data/
    └── messy_netflix_titles.csv
```


## Task

Write a script that cleans this specific Netflix dataset.

- Add the new cleaning functions to `class6_7_netflix_utils.py`.
- Update `class6_7_netflix_pipeline.py` to control the complete cleaning workflow.

Your program should:

1. Load the Netflix data.
2. Save a copy before cleaning.
3. Remove exact duplicate rows.
4. Remove rows containing missing values.
5. Remove `runtime_minutes` outliers using IQR.
6. Clean the `title`, `type`, and `country` columns.
7. Print a cleaning report.

**Complete the TODOs.**

### Step 1 — Update `class6_7_netflix_utils.py`

Add `re` and `pandas` to the imports at the top of the existing utility module. Then add the following functions below the Class 6 functions.

```python
import re

import pandas as pd

def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    # Strip surrounding whitespace.
    # Convert text to lowercase.
    # Collapse repeated whitespace.
    pass


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    pass
```

### Step 2 — Update `class6_7_netflix_pipeline.py`

Open the pipeline file that you completed in Class 6. 

1. Keep all the Class 6 code, including the argument parsing, logging setup, file loading, overview, duplicate removal, and missing-row removal.
2. Update the existing import from `class6_7_netflix_utils` so it includes the new functions:

```python
from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)
```

3. Immediately after loading the CSV file, save a copy of the original DataFrame:

```python
df_original = df.copy()
```

4. After the existing `drop_missing_rows()` section, complete the following TODOs:

```python
    # TODO 3:
    # Inside a try block, remove runtime_minutes outliers
    # using remove_iqr_outliers() with a threshold of 1.5.
    # Catch ValueError and exit with sys.exit(1).# Log an INFO message.

    # TODO 4:
    # Apply clean_text() to title, type, and country.
    # Log an INFO message.

    # TODO 5:
    # Create a report (dictionary) containing rows_before, rows_after, rows_removed, and columns.
    # Log an INFO message reporting: rows_before, rows_after, rows_removed, and columns.
    
```

## Try These Commands

```bash
python class6_7_netflix_pipeline.py
python class6_7_netflix_pipeline.py --verbose
python class6_7_netflix_pipeline.py --input data/missing.csv
```



## Expected Output

Using the provided dataset, your output should include:

```text
10:15:02 INFO     __main__ — Loaded 25 rows and 7 columns
10:15:02 INFO     __main__ — Displayed DataFrame overview
10:15:02 INFO     __main__ — Removed 1 duplicate row(s)
10:15:02 INFO     __main__ — Dropped 7 rows with missing values
10:15:02 INFO     __main__ — Removed 1 runtime_minutes outlier(s)
10:15:02 INFO     __main__ — Cleaned text column: title
10:15:02 INFO     __main__ — Cleaned text column: type
10:15:02 INFO     __main__ — Cleaned text column: country
10:15:02 INFO     __main__ — Cleaning complete: {'rows_before': 25,'rows_after': 16, 'rows_removed': 9, 'columns': 7}
```

With `--verbose`, the output should also include DEBUG messages from `class6_7_netflix_utils`.



## Save Your Work to GitHub

```bash
git status
git add class6_7_netflix_utils.py class6_7_netflix_pipeline.py
git commit -m "Complete the Class 6-7 Netflix pipeline"
git push
```

---
