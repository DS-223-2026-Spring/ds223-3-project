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
ds223-3-project/
│   .gitignore
│   CONTRIBUTING.md
│   docker-compose.yml
│   mkdocs.yml
│   README.md
│
├── api/                    ← Ani
│   │   Dockerfile
│   │   requirements.txt
│   └── app/
│       │   main.py
│       │   database.py
│       ├── models/
│       │       schemas.py
│       └── routers/
│               quiz.py
│               recommend.py
│               segments.py
│               studios.py
│               users.py
│
├── app/                    ← Maria
│       app.py
│       Dockerfile
│       requirements.txt
│       pages/
│
├── db/                     ← Liana 
│       init.sql
│
├── etl/                    ← Hmayak
│       connection.py
│       config.py
│       Dockerfile
│       orchestration_plan.md
│       flows/
│           load_data.py
│           train_model.py
│           validate_data.py
│           generate_recommendations.py
│
├── ds/                  ← Meline
│       Dockerfile
│       requirements.txt
│       notebooks/
│       scripts/
│       data/
│       models/
│
├── data/                   ← shared CSVs
│
├── Milestone1/             ← deliverables
│
└── docs/                   ← mkdocs


## Review Expectations
- PRs reviewed within 24 hours of being opened
- Reviewer (Anna) checks: docstrings present, no direct main commits, branch matches role, commit messages are descriptive
- Approvals require either: passing manual test of the changed service, or a clear note in the PR explaining why the change is non-functional
- Conflicts must be resolved by the PR author before review