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
│   .env.example
│   .gitignore
│   CONTRIBUTING.md
│   docker-compose.yml
│   LICENSE
│   mkdocs.yml
│   README.md
│
├───activityhub
│   │   __init__.py
│   │
│   ├───api                    ← Ani
│   │   │   Dockerfile
│   │   │   README.md
│   │   │   requirements.txt
│   │   │
│   │   └───app
│   │       │   database.py
│   │       │   main.py
│   │       │   __init__.py
│   │       │
│   │       ├───models
│   │       │       schemas.py
│   │       │       __init__.py
│   │       │
│   │       └───routes
│   │               quiz.py
│   │               recommend.py
│   │               segments.py
│   │               studios.py
│   │               users.py
│   │               __init__.py
│   │
│   ├───app                    ← Maria
│   │   │   app.py
│   │   │   Dockerfile
│   │   │   README.md
│   │   │   requirements.txt
│   │   │
│   │   └───pages
│   │           1_Quiz.py
│   │           2_Recommendations.py
│   │           3_Studio_Dashboard.py
│   │
│   ├───db                     ← Liana 
│   │      connection.py
│   │      crud.py
│   │      Dockerfile
│   │      init.sql
│   │      load_data.py
│   │      requirements.txt
│   │   
│   │
│   ├───ds                  ← Meline
│   │   │   Dockerfile
│   │   │   README.md
│   │   │   requirements.txt
│   │   │
│   │   ├───data
│   │   │       classes.csv
│   │   │       studios.csv
│   │   │       survey.csv
│   │   │       training_survey.csv
│   │   │       training_survey_augmented.csv
│   │   │
│   │   ├───models
│   │   │       metrics.csv
│   │   │       style_classifier.pkl
│   │   │
│   │   ├───notebooks
│   │   │       01_eda.ipynb
│   │   │
│   │   └───scripts
│   │           augment_training.py
│   │           generate_all_data.py
│   │           prepare_survey.py
│   │           train_model.py
│   │           train_model.py.save
│   │
│   ├───etl                    ← Hmayak
│   │   │   .Rhistory
│   │   │   config.py
│   │   │   connection.py
│   │   │   Dockerfile
│   │   │   orchestration_plan.md
│   │   │   README.md
│   │   │   requirements.txt
│   │   │
│   │   └───flows
│   │           generate_recommendations.py
│   │           load_data.py
│   │           pipeline.py
│   │           train_model.py
│   │           validate_data.py
│   │           __init__.py
│   │
│   └───shared
│          README.md
│          recommend.py
│          __init__.py
│
├───docs                   ← mkdocs
│   │   api.md
│   │   architecture.md
│   │   database.md
│   │   ds.md
│   │   frontend.md
│   │   index.md
│   │   orchestration.md
│   │   README.md
│   │
│   └───imgs
│           ActivityHub_model_ERD.png
│           project_architecture_diagram.svg
│
└───Milestone1
        ActivityHub_UI_Prototype.pdf
        MoSCoW.png
        Problem_Definition.pdf
        Product_Roadmap.pdf
        project_architecture_diagram.svg
        Roadmap_Flowchart.png
        UI_Prototype.html


## Review Expectations
- PRs reviewed within 24 hours of being opened
- Reviewer (Anna) checks: docstrings present, no direct main commits, branch matches role, commit messages are descriptive
- Approvals require either: passing manual test of the changed service, or a clear note in the PR explaining why the change is non-functional
- Conflicts must be resolved by the PR author before review