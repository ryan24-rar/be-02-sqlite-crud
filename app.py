import sqlite3

from flask import Flask,request,jsonify

app= Flask(__name__)


def init_db():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            done INTEGER NOT NULL DEFAULT 0
                   )
                   
             """)
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    if task_count ==0:

        starter_tasks= [
            ("Learn task A", 0),
            ("Learn task B", 0),
            ("Learn task C", 0)
        ]

        cursor.executemany(
            "INSERT INTO tasks (title,done) VALUES (?,?)",
            starter_tasks
        )
    
    connection.commit()
    connection.close()


init_db()


@app.route("/tasks", methods=(["GET"]))
def get_tasks():
    connection=sqlite3.connect("tasks.db")
    connection.row_factory=sqlite3.Row
    cursor = connection.cursor()


    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    tasks = [dict(row) for row in rows]

    connection.close

    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(dict(row))

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if data is None or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"].strip()

    if title == "":
        return jsonify({"error": "Title is required"}), 400

    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, 0)
    )

    task_id = cursor.lastrowid
    connection.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid request"}), 400

    title = data.get("title")
    done = data.get("done")

    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        connection.close()
        return jsonify({"error": "Task not found"}), 404

    new_title = title if title is not None else existing_task["title"]
    new_done = done if done is not None else existing_task["done"]

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, int(new_done), task_id)
    )

    connection.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Task not found"}), 404

    connection.commit()
    connection.close()

    return jsonify({"message": "Task deleted"})




    updated_task = cursor.fetchone()
    connection.close()

    return jsonify(dict(updated_task))


    new_task = cursor.fetchone()
    connection.close()

    return jsonify(dict(new_task)), 201




if __name__=="__main__":
    app.run()

