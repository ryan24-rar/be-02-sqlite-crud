# A2 — SQLite Task CRUD API

## Project Overview

This project is a CRUD REST API built with Python, Flask, and SQLite.

The API allows users to:

- Create tasks
- Read all tasks
- Read one task by ID
- Update tasks
- Delete tasks

The task data is stored in a SQLite database, so the data remains saved after the Flask server is stopped and restarted.

## Technologies Used

- Python
- Flask
- SQLite
- SQL
- JSON
- PowerShell for API testing

## Why SQLite Was Chosen

SQLite was chosen because it is lightweight and easy to use.

It does not require a separate database server. The full database is stored in one file, which makes it suitable for a small project like this assignment.

Python also includes the sqlite3 library, so no separate SQLite package is needed.

## Database Location

The SQLite database is stored in the project folder as:

tasks.db

| Column  | Type    | Description                                           |
| ------- | ------- | ----------------------------------------------------- |
| `id`    | Integer | Unique ID for each task                               |
| `title` | Text    | The task title                                        |
| `done`  | Integer | Completion status: `0` means false and `1` means true |



# How to Run 

Create Virtual Environment: `py -m venv venv`

Activate it : `.\venv\Scripts\Activate.ps1`

install packages : `python -m pip install -r requirements.txt`

Start the app : `python app.py`

The API runs at: `http://127.0.0.1:5000`



# API Endpoints

GET    /tasks
GET    /tasks/<id>
POST   /tasks
PUT    /tasks/<id>
DELETE /tasks/<id>







