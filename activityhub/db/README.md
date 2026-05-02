# Database Service

PostgreSQL 17 service for ActivityHub.

## Files
- `init.sql` — schema (runs on container init)
- `connection.py` — DB connection helpers
- `crud.py` — generic insert/select/update/delete with table allowlist
- `load_data.py` — bulk CSV loader (studios, classes)

## Schema (8 tables)
| Table | Purpose |
|---|---|
| `users` | Quiz takers |
| `quiz_responses` | Per-user preference snapshot |
| `studios` | 23 Yerevan studios |
| `classes` | 159 classes |
| `segments` | K-means user personas (M3) |
| `user_segments` | many-to-many user↔segment |
| `recommendations` | Model output history |
| `bookings` | "I tried this class" feedback (M3) |

## Run
```bash
docker compose up -d db
```

Reset: `docker compose down -v && docker compose up -d db`

## Verify
```bash
docker compose exec db psql -U admin -d activityhub -c "SELECT COUNT(*) FROM studios;"
```
Should print 23 after ETL runs.

## CRUD usage
```python
from db.connection import get_session
from db.crud import select_all
session = get_session()
studios = select_all(session, "studios")
session.close()
```

Only tables in `ALLOWED_TABLES` (in `crud.py`) can be written to.

