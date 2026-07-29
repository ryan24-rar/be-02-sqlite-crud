import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)

            cursor.execute("SELECT COUNT(*) AS count FROM tasks")
            task_count = cursor.fetchone()["count"]

            if task_count == 0:
                cursor.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    [
                        ("Learn task A", False),
                        ("Learn task B", False),
                        ("Learn task C", False)
                    ]
                )


def get_all_tasks():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks ORDER BY id")
            return cursor.fetchall()


def get_task_by_id(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tasks WHERE id = %s",
                (task_id,)
            )
            return cursor.fetchone()


def create_task(title):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING *
                """,
                (title, False)
            )
            return cursor.fetchone()


def update_task(task_id, title, done):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                RETURNING *
                """,
                (title, done, task_id)
            )
            return cursor.fetchone()


def delete_task(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s",
                (task_id,)
            )
            return cursor.rowcount > 0