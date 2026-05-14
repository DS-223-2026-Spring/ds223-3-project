# ActivityHub

A personalized activity matching platform for Yerevan that connects users with yoga, dance, and fitness studios based on personality, schedule, and budget.

## Problem

Discovering the right extracurricular class in Yerevan is hard. Users browse Instagram pages, ask friends, and try classes that often don't fit their energy level, schedule, or budget. Studios meanwhile struggle to reach the right audience.

## Solution

A 2-minute onboarding quiz feeds a multi-class ML model that predicts which of 9 style buckets a user is most likely to enjoy — across all activities, not just one they thought they wanted. The top 3 matches are surfaced with explanations, and a "I tried this" button feeds back into model retraining.

For studio owners, a separate dashboard exposes K-means user segments and booking-likelihood estimates.

## Expected Outcomes

- Users discover classes they wouldn't have searched for themselves
- Studios get audience insights without needing their own analytics stack
- A reproducible end-to-end ML pipeline (data → train → segment → serve) that retrains on real user feedback over time

## Architecture
The product runs as a microservice stack - see [Architecture](architecture.md) for details:

- **api** - FastAPI backend
- **app** - Streamlit frontend
- **db** - PostgreSQL
- **ds** - scikit-learn classifier + segmentation
- **etl** - Prefect data pipeline (Orchestration)

## Quick start

```bash
docker compose up --build
```

Visit http://localhost:8501 for the user-facing app, http://localhost:8000/docs for API documentation.

## What it looks like

![ActivityHub recommendations](imgs/recommendations.png)

## Documentation

See sections in the left nav for each component.