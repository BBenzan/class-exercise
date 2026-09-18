# DS3500 _Fall 2026_ 
# Class 1: Introduction and Git, GitHub


## Learning Objectives:
By end of today's class, you will be able to:
1. Understand the course expectations
2. Describe what we will learn throughout the semester
3. Explain Git/GitHub
4. Run core Git commands

---

### Part 1: Course Introduction 
- The Goal: Throughout this course, we won't just learn how to code. We'll learn how to build DS systems -- systems that are production-ready, reusable, and presentable. 

**Two Final Project Tracks:**
```
1. End-to-End ML Platform -- I build a full ML system, not just a model! I.e., I build an application where users may enter data, the model makes a prediction, and the result is shown to the user.

2. Visualization Platform -- I build scalable visualization systems, not just charts! I.e., I build an application where users can explore data and interact with the results.
```
Reminder: You'll choose ONE in Week 11. But first, we'll build together the foundations and skills that work for ALL tracks.


**The Building Block Strategy**
```
Week 5:  Mini-Prototype 1 (Data Pipeline)
            ↓
Week 8:  Mini-Prototype 2 (API)
            ↓
Week 11: Mini-Prototype 3 (Database + Cache)
            ↓
Week 14: Final Project (Integrate + Specialize)
```

**Expected Outcome:**
- Until Week 11, you'll build 3 mini-prototypes (foundations)
- In Week 11, choose your track so that your final project integrates the mini-prototypes + track-specific features
- Everything you've done in this course will stay in your Github account -- for your resume and portfolio. 

**Keep in mind:** We’ll be busy learning and applying new concepts throughout the course. By the end, you’ll have a strong portfolio and practical skills.


**Syllabus:** Review the full course syllabus under the main page on Canvas.
- Course schedule
- Important dates for quizzes, presentations, etc.
- Assignment deadlines and requirements
- Grading policies
- Plagiarism and cheating
- etc.

#### Typical Class Structure
- Each class will be dedicated to learning the topics for each MP/final project.
- We will do lots of coding together.
- TAs will join us to provide in-class support.


#### Complete the First-day-of-class survey
- Link: https://forms.gle/fwwrKeNht5YSGyau9

---


### Part 2: GitHub Account Setup
- If you do not have an account, go to the website `github.com` and create one.
- If you already have a GitHub account or once you create one, complete the survey: https://forms.gle/CgRfB85SaF6Bs4Yu5 

---

### Part 3: Git Setup

For Windows,
1. Open the Command Prompt or PowerShell.
2. Type `git --version` and press Enter.
3. If you don't have one, visit the official Git Website `https://git-scm.com/install/windows` and choose one of installation methods.

For Mac,
1. Open the Terminal app.
2. Type `git --version` and press Enter.
3. If you don't have one, type the following command on Terminal and press Enter `xcode-select --install`. Alternatively, you can visit the official website at `https://git-scm.com/install/mac` and choose another installation method.


**Configure Git username and email**
```bash
# Set your name or username
git config --global user.name "<your_name>"
# Set your GitHub-matched email
git config --global user.email "<your_GitHub_email_address>"
```

check your configurations!
```bash
git config user.name
git config user.email
```

---

### Part 4: Introduction to Git and GitHub

**What is Git?**
Git is an open-source program that handles the version control system and runs locally. Think about Google Doc Version History -- it tracks all the changes and lets you see and restore earlier versions.

**Why it matters:**
- Track your progress without you creating a bunch of copies.
- Industry standard: Job openings may look for Git experience

Git Terminology and Workflow (quiz)
1. Working Directory: The actual folder where you edit your files.
2. Staging Area: A hidden checklist of changes ready to commit.
3. Repository: The permanent database of your snapshots.

```
Edit files  →  git add  →  git commit
    ↓             ↓            ↓
Working        Staging      Repository
```

Basic commands (quiz):
- `git status` - Check the status 
- `git add <file>` - Move the file in Working Directory to Staging 
- `git commit -m "message"` - Move the file in Staging Area to Repository
- `git log` - View history


#### Git Basics
Let's create our first Git repository together
```bash
# Navigate to the folder where you want to create your project (e.g., your class folder), then create a new folder:
mkdir class-exercise
cd class-exercise

# Initialize Git; it creates hidden .git folder tracking changes
git init 

# Check status
git status

# Create a Python file
## you can just create a new file in a text editor/IDE.
## or run a command line
## Mac: nano class1_git_demo.py 
## Windows: notepad class1_git_demo.py 

# Check status again; now we have an "untracked file"
git status

# Add file to staging
git add class1_git_demo.py
git status # file is now "staged" (ready to save)

# Commit (save snapshot); -m is message describing what you did
git commit -m "Created a new file"

# View history
git log
#or git log --oneline

# Add print(3500) in the py file

# Add file to staging
git add class1_git_demo.py
git status # file is now "staged" (ready to save)

# Commit (save snapshot); -m is message describing what you did
git commit -m "Added print(3500)"

# View history
git log
#or git log --oneline
```


#### Connect your local Git repository to GitHub

**What is GitHub?**
- Git = Local version control
- GitHub = Cloud storage, collaboration

#### GitHub setup
0. Setup: you have a local repo called `class-exercise`. You are going to connect your local Git repository to GitHub
1. Create new repo on GitHub: use the same repo name
    - Log in to github.com.
    - Click the + icon in the top-right corner
    - Select New repository. Repository name: Use the exact same name as your local folder: class-exercise
    - Set the visibility to Public 
    - No need to check any other boxes
    - Create Repo
2. On the next screen, 
    - look for the section titled "…or push an existing repository from the command line". 
3. Copy and paste those three commands into your Terminal/Command Prompt/PowerShell one by one.
    - Note: The first time you push to GitHub, you may be asked to authenticate your GitHub account 
    For example,
    ```
    username for 'https://github.com':  ENTER YOUR GITHUB USERNAME
    password for 'https://<username>@github.com': ENTER YOUR PAT
    ```
    - To obtain PAT: Go to Settings > Developer settings > Personal access token > Tokens (classic)
4. Refresh GitHub - code is there!



**What does each line mean?**

1. git remote add origin https://github.com/...
    - Purpose: Connects your local Git repository to a remote repository (on GitHub in this case).
    - Effect: After this command, your local repo "knows" where to push and pull code from.
    - What is origin? When you run the command git remote add origin https://github.com/..., you are telling Git: "Hey computer, instead of making me type out this super long GitHub URL every single time, let's just create a shortcut nickname and call it origin." origin is simply the standard, default nickname the software industry uses for your primary central server in the cloud.

2. git branch -M main
    - Purpose: Renames your current branch to main.
    - What is the main branch? A Git repository can have multiple timelines or tracks of development, which are called branches. main is the name of your primary timeline where the final production-ready code lives. We will learn more about branches next week.


3. git push -u origin main
    - Purpose: Push your local main branch to the remote repository on GitHub.
    - Effect: After this command, your code appears on GitHub under the main branch, and your local branch is _linked_ to track the remote branch for easy updates. So, you only need -u the first time you push a new local branch.


 
#### The Workflow Between Git (Local) and GitHub (Remote) 

It is crucial to understand that the Local Repository (in your computer) and the Remote Repository (on GitHub) are completely separate environments. 

Code updates are never automatic; you must move them through three distinct stages:
- git add (staging): This tells Git which specific changes you want to include in your next save point.
- git commit (commit): This creates a permanent, secure snapshot of your project inside your local computer's repository. Note: Your code is still only on your laptop and has not reached the internet yet.
- git push (push): This uploads all the local snapshots you've recorded from your computer straight to your GitHub remote repository. Once this step is complete, your code is live on the web.

**Let's practice pushing to GitHub**
```bash
# Step 0 - local : Update the file -- open it and add print(10) 

# Step 1- local : Stage the modified file
git add class1_git_demo.py
# Step 2- local : Save a snapshot of your project to your local computer (write a clear message!)
git commit -m "add print(10)"

# Step 3- remote : Upload your saved local changes to your GitHub remote repository
git push # now Git knows where to push.
```

