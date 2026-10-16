# GitHub Upload Guide — CreatorLedger

## Before uploading
- Use this project folder, not your old backup folder.
- Keep `.venv/`, local database files (`creatorledger.db`, `*.sqlite`, `*.sqlite3`), and secrets out of GitHub. The `.gitignore` already excludes them.
- Review the screenshot folder. Screenshots can contain other desktop windows; use only screenshots you are comfortable publishing. Replace them with clean app-only screenshots if needed.
- This is an educational local prototype. It does not include authentication or multi-user data isolation. Do not deploy it publicly with real client data.

## Steps (Windows / VS Code)
1. Create a new repository on GitHub named `creatorledger`.
2. Choose Public or Private as your instructor requires. Do not add a README, license, or `.gitignore` on GitHub because this folder already has project files.
3. In VS Code, open the extracted `creatorledger` project folder.
4. Open Terminal and run:

```powershell
git init
git add .
git status
git commit -m "Prepare CreatorLedger project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/creatorledger.git
git push -u origin main
```

5. Replace `YOUR-USERNAME` with your actual GitHub username and use the exact repository URL GitHub shows.
6. Before `git commit`, check `git status` and ensure no database, `.venv`, `.env`, or private client records are listed.
7. Refresh the GitHub repository page and confirm README, app.py, templates, static files, tests, and documentation are visible.

## If Git says the remote already exists
Run `git remote -v` first. If it points to the correct repository, skip `git remote add origin` and continue with `git push -u origin main`. Do not remove a remote unless you understand what it points to.

## Run tests before submission
After installing dependencies in the project virtual environment:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Only report tests as passed if the command finishes with `OK`.
