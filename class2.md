# Weekly Announcements
* **MP 1** is posted on Canvas under **Assignments**.
    * MP 1 - Part 1 is available. 
* **MP1-WSU 1** is due on Friday (9/18) and will be available the night before.
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
* AI policy has been updated -- see the syllabus for more details!

---

# Our goal for the next 4 weeks
**MP1: End-to-End Data Pipeline**

In MP1, we will build an end-to-end command-line data pipeline that loads, validates, cleans, and saves data.

We will start by building the basic pipeline structure and then extend the same repository throughout four parts. 

Through this, we will practice organizing Python code into modules, working with file paths and different file formats, using logging for errors and status updates, managing a project with Git and GitHub, and integrating multiple components into a single working application.

---

# Class 2: CLI Tools and Logging

## Learning Objectives

By the end of today's class, you will be able to:

1. Build Python scripts that accept command-line arguments.
2. Use `argparse` to create professional CLIs.
3. Use Python's `logging` module to monitor and understand program behavior.
4. Choose the appropriate logging level for different situations.

---

# Part 1: Command-Line Arguments

## Why Use Command-Line Arguments?

So far, I/we have run Python programs by simply specifying the script:

```bash
python analyze.py
```

But professional programs often need to work with different inputs and settings.

For example:

```bash
python analyze.py --input sales_2024.csv --output report.json
```

The same program can now work with different files without changing the code.

---

## Argument Parser: `argparse` (quiz)

`argparse` makes it easy to build command-line interfaces (CLIs).

```python
#class2_argparse_demo.py
import argparse

# Create an ArgumentParser
parser = argparse.ArgumentParser(
    description="Analyze a data file"
)

# Add a named argument (required)
parser.add_argument(
    "--input", "-i",
    required=True,
    help="Path to input CSV file"
)

# Add named arguments (optional)
parser.add_argument(
    "--output", "-o",
    default="results.txt",
    help="Output file path"
)

parser.add_argument(
    "--verbose", "-v", 
    action="store_true", 
    help="Print detailed information"
    # Note 1: verbose has its default value as False
    # Note 2: action="store_true" sets this to True.
)

# Parse the command-line arguments
args = parser.parse_args()
# e.g. args.input , args.output, args.verbose
```

### Running the Program

1. Show help:
```bash
python class2_argparse_demo.py --help
```

2. Provide the required argument:
```bash
python class2_argparse_demo.py --input sales.csv
```

3. Specify an output file:
```bash
python class2_argparse_demo.py --input sales.csv --output report.txt
```

4. Use the short form:
```bash
python class2_argparse_demo.py -i sales.csv -o report.txt
```

5. Use a boolean flag:
```bash
python class2_argparse_demo.py --input sales.csv --verbose
# Or python class2_argparse_demo.py --input sales.csv -v
```

### Key Ideas
* `ArgumentParser` creates the command-line interface.
* Named arguments can be required or optional.
* Named arguments begin with `--`. Short forms can be added with `-`.
* `default` specifies a value when an option is not provided.
* `--help` is automatically generated.

---

# Try It Yourself 1 — Build a CSV Data Checker CLI

### Before You Start

Open your **`class-exercise`** folder (the folder you created and connected to GitHub in Class 1).

Inside the folder, create a new Python file named:

```text
class2_data_checker.py
```

Also, place the `students.csv` file inside the folder.

You will build a command-line tool that checks the quality of a CSV file.

### Task

Use `argparse` to:

1. Accept a CSV filename from the command line.
2. Accept an optional output filename.
3. Accept a `--verbose` / `-v` flag.
4. Check whether the input file exists.
5. Read the CSV file and check for missing values.
6. Save the results to the output file.

The CSV-processing code is provided.


**Complete the TODOs.**

```python
import argparse
import csv
import sys
from pathlib import Path


def check_data(filename):
    """Read the CSV file and check for missing values."""
    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]
    missing_rows = []

    for row_number, row in enumerate(data, start=2):
        if any(value == "" for value in row):
            missing_rows.append(row_number)

    return header, data, missing_rows

# TODO 1: Create an ArgumentParser
# Description: "Check the quality of a CSV file."


# TODO 2: Add a named argument (required):
# Long form: --input
# Short form: -i
# Help: "CSV file to check"


# TODO 3: Add an named argument (optional):
# Long form: --output
# Short form: -o
# Default: "data_quality.txt"
# Help: "Output report filename"


# TODO 4: Add a boolean flag:
# Long form: --verbose
# Short form: -v
# Use action="store_true"
# Help: "Show detailed DEBUG messages"


# TODO 5: Parse the command-line arguments


# Check if the file exists 
p = Path(args.input)
if not p.is_file():
    print(f"File not found: '{args.input}'")
    sys.exit(1)

print(f"File validated: '{args.input}'")

# Check the data
header, data, missing_rows = check_data(args.filename)

# Save the report
with open(args.output, "w") as f:
    f.write(f"Number of rows: {len(data)}\n")
    f.write(f"Number of columns: {len(header)}\n")
    f.write(f"Number of rows with missing values: {len(missing_rows)}\n")
```

### Try These Commands

```bash
python class2_data_checker.py --input students.csv
```

```bash
python class2_data_checker.py --input students.csv --output report.txt
```

### Save Your Work to GitHub

When you finish:

```bash
git status
git add class2_data_checker.py
git commit -m "Complete CSV data checker CLI"
git push
```

> **Note:** Do not worry about `students.csv`/`data_quality.txt` showing as untracked. We will take care of this issue in the next class.

---

# Part 2: Logging

## Why Use Logging?

`print()` is useful for simple output, but professional programs often need more control over what they report.

With `print()`:

* No timestamps
* No severity levels
* Difficult to control which messages are shown
* Not designed for monitoring larger or long-running programs

> `logging` allows us to control what information the program reports and how important that information is.

---

## Basic Logging Example

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)

# Create a module-level logger
logger = logging.getLogger(__name__)

x = 42

logger.info("Loading file...")
logger.debug("Processing row 1...")
logger.debug(f"Value is {x}")
logger.info("Done!")
```

Expected Output:

```bash
13:25:58 INFO     Loading file...
13:25:58 DEBUG    Processing row 1...
13:25:58 DEBUG    Value is 42
13:25:58 INFO     Done!
```
---

## Logging Levels (quiz)

Python provides five common logging levels:

|     Level    | Meaning                                                         | Example                                          |
| :----------: | :-------------------------------------------------------------- | :----------------------------------------------- |
| **CRITICAL** | A very serious problem; the program cannot continue | `logger.critical("Database connection failed")`  |
|   **ERROR**  | A specific operation failed; the program may or may not be able to continue                                     | `logger.error("Could not read input file")`      |
|  **WARNING** | Something unexpected happened, but the program can continue     | `logger.warning("120 rows have missing values")` |
|   **INFO**   | Normal program progress                                         | `logger.info("Loaded 50,000 rows")`              |
|   **DEBUG**  | Detailed information for debugging                              | `logger.debug("Processing row 1")`               |

---

## Logging Levels Control What You See

The logging level determines which messages are displayed.

* `CRITICAL` → CRITICAL only
* `ERROR` → ERROR, CRITICAL
* `WARNING` → WARNING, ERROR, CRITICAL
* `INFO` → INFO, WARNING, ERROR, CRITICAL
* `DEBUG` → DEBUG, INFO, WARNING, ERROR, CRITICAL

For example, during development:

```python
level=logging.DEBUG
```

In production:

```python
level=logging.INFO
```

The advantage is that we can control how much information is displayed **without removing our logging statements**.

---

# Try It Yourself 2 — Add Logging to Your CSV Data Checker

## Before You Start

Before adding logging, make sure that you have **committed and pushed the working version of your program** from Try It Yourself 1.

---

## Add Logging

Let's continue working with the **`class2_data_checker.py`** file.

### Step 1: Import `logging`

Add:

```python
import logging
```

to your imports.

---

### Step 2: Set Up Logging

Add the following code **before creating your `ArgumentParser`**:

```python
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
# Create a module-level logger
logger = logging.getLogger(__name__)
```

---
### Step 3: Control the Logging Level

You already have a `--verbose` / `-v` argument.

If `--verbose` is provided, set the logger level to `DEBUG`:

After:

```python
args = parser.parse_args()
```

Add the following code:

```python
if args.verbose:
    logger.setLevel(logging.DEBUG)
```

This means:

* Without `--verbose` → show `INFO` and above.
* With `--verbose` → show `DEBUG` and above.
---

### Step 4: Log the Parsed Argument at the DEBUG level

After Step 3, add a DEBUG message showing the input filename.

For example:

```text
DEBUG Arguments parsed: filename=students.csv
```
---

### Step 5: Replace the File Check

Replace your existing file-checking code:

```python
p = Path(args.input)
if not p.is_file():
    print(f"File not found: '{args.input}'")
    sys.exit(1)

print(f"File validated: '{args.input}'")
```

with:

```python
p = Path(args.input)
if not p.is_file():
    logger.error(f"File not found: '{args.input}'")
    sys.exit(1)
    
logger.info(f"File validated: '{args.input}'")
```

---

### Step 6: Log Before Loading the Data

Before:

```python
header, data, missing_rows = check_data(args.input)
```

add a DEBUG message.

For example:

```text
DEBUG Loading data from: students.csv
```

---

### Step 7: Log the Number of Rows

After:

```python
header, data, missing_rows = check_data(args.input)
```

add an INFO message showing the number of rows loaded.

For example:

```text
INFO Loaded 5 rows
```

---

### Step 8: Handle an Empty Dataset

If the CSV file contains a header but **no data rows**, log an ERROR message and stop the program.

After code from Step 7, add:
```python
if len(data) == 0:
    logger.error("Input file contains no data; cannot continue")
    sys.exit(1)
```

---

### Step 9: Log Rows with Missing Values

After code from Step 8, add:

```python
for row_number in missing_rows:
    pass
```
Replace `pass` with a WARNING message.

For example:
```text
WARNING Row 1 has missing values
WARNING Row 3 has missing values
```

---

### Step 10: Log After Saving the Report

After the report is saved, add an INFO message.

For example:

```text
INFO Report saved to data_quality.txt
```

---

## Try These Commands

Without `--verbose`:

```bash
python class2_data_checker.py --input students.csv
```

Expected output
```text
10:30:12 INFO     File validated: 'students.csv'
10:30:12 INFO     Loaded 5 rows
10:30:12 WARNING  Row 4 has missing values
10:30:12 WARNING  Row 6 has missing values
10:30:12 INFO     Report saved to data_quality.txt
```

With `--verbose`:

```bash
python class2_data_checker.py --input students.csv --verbose
```
Expected output
```text
10:30:12 DEBUG    Arguments parsed: filename=students.csv
10:30:12 INFO     File validated: 'students.csv'
10:30:12 DEBUG    Loading data from: students.csv
10:30:12 INFO     Loaded 5 rows
10:30:12 WARNING  Row 4 has missing values
10:30:12 WARNING  Row 6 has missing values
10:30:12 INFO     Report saved to data_quality.txt
```

Test a missing file:

```bash
python class2_data_checker.py --input missing.csv
```
---

## Save Your Work to GitHub

When you finish:

```bash
git status
git add class2_data_checker.py
git commit -m "Add logging to CSV data checker"
git push
```

---