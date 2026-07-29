# Task API — PostgreSQL with Docker

A Flask CRUD API for tasks using PostgreSQL in Docker.

For A3, the storage was changed from SQLite to PostgreSQL. The routes and API behavior stayed the same. All database code is inside `postgres_repository.py`.

## Run the project

1. Copy `.env.example` to `.env`.
2. Make sure Docker Desktop is running.
3. Run:

```bash
docker compose up --build