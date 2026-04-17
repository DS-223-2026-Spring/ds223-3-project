# Contributing Guidelines

## Branch Names
Each team member works on their assigned branch:
- `db` — Liana (Database Developer)
- `back` — Ani (Backend Developer)
- `front` — Maria (Frontend Developer)
- `ds` — Meline (Data Scientist)
- `orch` — Hmayak (Automation Engineer)

## Before Starting Work
Always sync your branch with the latest main:

git checkout main
git pull origin main
git checkout your-branch
git merge main

## Commit Messages
I'm fine with anything loves. Just a bit of context. 

Good:
- Add database schema
- Fix connection timeout issue
- Update Streamlit quiz layout
- Remove unused imports

Bad:
- changes
- stuff
- updated things
- asdfgh

## Pull Request Process
1. Push your work to your branch: `git push origin your-branch`
2. Go to GitHub and click "Compare & pull request"
3. Set base branch to `main`
4. Write a short title describing what changed
5. Add a brief description if needed
6. Request review from Anna (@awinnnie)
7. Wait for review and approval before merging

## Rules
- Never push directly to main
- Never merge your own PR — Anna reviews and merges
- Pull main and merge into your branch before starting new work
- One feature or task per PR — don't bundle unrelated changes
- Add docstrings to all Python functions

## File Naming
- Python scripts: `load_data.py`, `train_model.py`
- Notebooks: `01_eda.ipynb`, `02_model.ipynb`
- Documentation: `README.md`, `API_DOCS.md`
- Data files: `studios.csv`, `synthetic_users.csv`

## Folder Structure
Each service has its own folder. Only work inside your assigned folder:

ds223-3-project/
data/           — shared CSV files (studios, classes, survey)
db/             — PostgreSQL setup, schemas, CRUD helpers
backend/        — FastAPI service
frontend/       — Streamlit app
ds/             — notebooks, scripts, models
orch/           — Prefect flows and config
docs/           — mkdocs documentation