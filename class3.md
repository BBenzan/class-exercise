# Weekly Announcements
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
    1. If you need help with Git/GitHub setup, fill out the form to get help.
* **Quiz 1 score** is available on Gradescope.
    1. The score is shown as a percentage, so you will need to convert it to points using the table provided in the syllabus. 
    2. All quiz scores will be collected at the end of the semester, and the final quiz grades will be posted on Canvas. In the meantime, please make sure to keep track of your progress.
* **MP 1** is posted on Canvas under **Assignments**.
    * MP 1 - Part 1 is available. 
* **MP1-WSU 1** is due on TODAY (Friday, 9/18).
    

## MP1-WSU 1
If you’re ready and would like to complete MP1-WSU 1 now, feel free to do so. 

---

# Class 3: Git Essentials: Ignore, Divide, Undo 

## Learning Objectives

By the end of today's class, you will be able to:
1. Use `.gitignore` to prevent Git from tracking specific files.
3. Create, switch between, and merge Git branches to develop features independently.
2. Use `git restore` to undo unwanted changes, whether or not they've been staged. 
4. Apply a branch-based workflow (branch → commit → merge → delete) to build a project incrementally.

> Note: All exercises we do in class are expected to be completed inside the class-exercise directory. Please make sure to navigate there (e.g., cd class-exercise) before starting any coding practice during class.

---

# Part 1: .gitignore

`.gitignore` tells Git what files to ignore. I.e., you use it when you don't want Git to track a file. 

**Common things to ignore**:
```
- Data files (too big)
- Log files
- Virtual environments
- IDE files
- Cache files
- Secrets (.env files)
- ...
```

Note: 
- Git can only ignore files that have never been tracked before.
- .gitignore doesn't get automatically generated or processed. You should configure it when necessary.
- You can add additional files or patterns to .gitignore as needed.


## Create .gitignore Together

```bash
# Go to the repo and Check status
cd class-exercise
git status
```

You should already have `students.csv` and other txt files sitting untracked in your `class-exercise` repo — we'll do `.gitignore` on those.

```bash
# Check all files including hidden
#Mac (terminal): ls -al 
#Windows (cmd.exe): dir /a
#       (PowerShell): ls -Force
#       (Git Bash): ls -al 
```

You may see hidden files like ., .., .DS_Store (for Mac), desktop.ini (for Windows), etc.

### Create a .gitignore file

- Create a new file using an IDE.

    - File name: .gitignore

    - Inside the file, Add:

```gitignore
# OS files
.DS_Store
desktop.ini
Thumbs.db

# Data files
*.csv
*.txt
data/

# Python caches & virtual envs
__pycache__/
*.pyc
.venv/
venv/

# IDE settings & Secrets
.vscode/
.idea/
.env
```


- Feel free to add any other files or folders you want to ignore as needed.

Run the following git commands:

```bash
git status
git add .gitignore
git commit -m "Add .gitignore"
git status
```



---

# Part 2: Git Branching

**Why branches?**

Work on features without breaking your main code.

**General Workflow**:

```
main: ──●────●────●────●────
           \
            ●────●────●  feature/data-loader
             (work here without affecting main)
```

## Git Branching Practice (quiz)

- Create an empty file named `class3_branch_demo.py`.
- Do git add and commit the file
```bash
git add class3_branch_demo.py
git commit -m "Add class3 branch demo"
```

**Visual workflow of this practice**
```
main branch
    │
    └── class3_branch_demo.py 

feature/add-print branch
    │
    └── class3_branch_demo.py (modified)
             │
          git merge
             ↓
main branch
    │
    └── class3_branch_demo.py (updated)
```

```bash
# Check current branch
git branch
# * main  ← The asterisk shows current branch and it already has class3_branch_demo.py

# Create and switch to a new branch
git switch -c feature/add-print

# Check again
git branch
#   main
# * feature/add-print  ← Now on new branch

# Make updates on class3_branch_demo.py (e.g. add a print statement)

# After print() is added, git add and commit
git add class3_branch_demo.py
git commit -m "Add print statement"

# See what's updated 
git diff main feature/add-print -- class3_branch_demo.py

# Switch back to main
git switch main

# Bring changes from feature branch to main
git merge feature/add-print

# Deletes feature branch
git branch -d feature/add-print

# View branch history
git log --oneline 
```

## Delete a Branch Without Merging

```bash
git switch main 
git branch -d feature/add-print # safe delete; refuses if the branch has unmerged __commits__
# OR 
git branch -D feature/add-print # force delete; deletes it even if it has unmerged __commits__
```

**When to use branches**:
- New feature
- Bug fix
- Experiment (might not keep)

**Best practices**:
- Keep branches short-lived
- Merge frequently
- Delete after merging

**Quick note on the prefix `feature/`**:

Using the `feature/` prefix is an industry best practice because it keeps your project organized, especially as your project grows.

When you look at a list of many branches in a big project, flat names get confusing. Prefixes tell you the intent of the branch instantly:
- `feature/add-print` (Building something new)
- `bugfix/login-error` (Fixing a broken problem)
- `hotfix/payment-crash` (An urgent fix needed on production)
- `docs/update-readme` (Just updating text files, no code changes)
- ...

## Merge Conflicts

If your main branch and feature branch *both* have changed the same line, Git can't automatically combine them — this is a conflict.

```bash
git merge feature/add-feature
# CONFLICT (content): Merge conflict in ...py
# Automatic merge failed; fix conflicts and then commit the result.
```

When this happens, open the file and See where Git marks the conflicting spot:

For example, 

```python
<<<<<<< HEAD
print("Welcome to DS 3500")
=======
print("Welcome to CS 2000")
>>>>>>> feature/add-feature
```

Edit the file to keep whichever version you want (or combine both), then:

```bash
git add file.py
git commit -m "Resolve merge conflict"
```

> **Note:** Changes on *different* lines merge automatically with no conflict — conflicts only happen when the same line is touched by both sides.

---
# Part 3: Git Restore

## Git Restore (quiz)
Use `git restore` to undo your changes when you accidentally ruin your code. Think of this command as your "Undo" button for physical files in your project.

### Scenario 1: You want to go back to the latest version (commit) and you haven't run git add yet

This is the most common scenario. You were editing main.py, the code got completely messy, and you want to wipe out all recent changes and go back to your last safe commit.

```bash
git restore main.py 
```

**Warning:** Everything you typed since your last commit disappears instantly. Your file returns to the exact state it was in when it was last saved.

### Scenario 2: You already ran git add by mistake

If you modified main.py and accidentally typed `git add main.py`, your ruined code is now sitting in the "Staging Area" (waiting to be committed). 

To fix this:

```bash
git restore --staged main.py # Unstaging
git restore main.py
```

## Git Revert/Reset: Going Back to any previous Commit

`git restore` undoes *uncommitted* changes. If the bad change is already committed, use one of these instead:

```bash
git log --oneline                      # find the commit hash you want
                                        # The hash is the short ID on the left (e.g., e565f5b)
                                        # Use that ID in <commit-hash> below.
git switch --detach <commit-hash>             # look around an old commit (temporary)
git revert <commit-hash>               # undo a commit safely (adds a new commit)
# or git reset --hard <commit-hash>         # rewind branch, discarding commits after it
```

> **Rule of thumbs**: `reset` is for your own mess before you've shared it; `revert` is for anything after you've shared it."

---

# Try It Yourself — Practice Git Branching with a Simple Calculator

**The idea:** We start with a simple calculator that only supports addition, then add one new operation per Git branch. The code for each step is small and given to you in full — the goal is to practice the **branch → implement → commit → merge → delete** workflow, not to write tricky logic.

---

### Step 1 — Initial Commit

In the `class-exercise`, create a new Python file, `class3_calculator.py`, and copy the following into the file:

```python
# class3_calculator.py
import argparse

def add(a, b):
    return a + b


def main():
    parser = argparse.ArgumentParser(description="A simple calculator")
    parser.add_argument("--a", "-a", type=float, required=True, help="First number")
    parser.add_argument("--b", "-b", type=float, required=True, help="Second number")
    parser.add_argument(
        "--operation", "-op",
        choices=["add"],
        default="add",
        help="Operation to perform"
    )
    args = parser.parse_args()

    if args.operation == "add":
        result = add(args.a, args.b)

    print(f"Result: {result}")


if __name__ == "__main__":
    main()
```

Commit this starting point to `main`:

```bash
git init
git add class3_calculator.py
git commit -m "Initial commit"
```

---

### Step 2 — Branch: `feature/subtract`

Create and switch to a new branch:

```bash
git switch -c feature/subtract
```

Make two changes to `class3_calculator.py`:

1. Add a `subtract` function above `main()`:

```python
def subtract(a, b):
    return a - b
```

2. Update the `--operation` choices and add a new `elif` branch inside `main()`:

```python
    parser.add_argument(
        "--operation", "-op",
        choices=["add", "subtract"],
        default="add",
        help="Operation to perform"
    )
```

```python
    if args.operation == "add":
        result = add(args.a, args.b)
    elif args.operation == "subtract":
        result = subtract(args.a, args.b)
```

Commit the feature, then merge it back into `main`:

```bash
git add class3_calculator.py
git commit -m "Implement subtract"
git switch main
git merge feature/subtract
git branch -d feature/subtract
```

---

### Step 3 — Branch: `feature/multiply`

Create and switch to a new branch:

```bash
git switch -c feature/multiply
```

Make two changes to `class3_calculator.py`:

1. Add a `multiply` function above `main()`:

```python
def multiply(a, b):
    return a * b
```

2. Update the `--operation` choices and add a new `elif` branch inside `main()`:

```python
    parser.add_argument(
        "--operation", "-op",
        choices=["add", "subtract", "multiply"],
        default="add",
        help="Operation to perform"
    )
```

```python
    elif args.operation == "multiply":
        result = multiply(args.a, args.b)
```

Commit the feature, then merge it back into `main`:

```bash
git add class3_calculator.py
git commit -m "Implement multiply"
git switch main
git merge feature/multiply
git branch -d feature/multiply
```

---

## Try These Commands

```bash
python calculator.py --a 5 --b 3
python calculator.py --a 5 --b 3 --operation subtract
python calculator.py --a 5 --b 3 --operation multiply
python calculator.py -a 5 -b 3 -op add
python calculator.py --b 3    # missing --a → argparse should show a "required" error
```

## Save Your Work to GitHub

When you finish:

```bash
git log --oneline
git status
git push
```

---