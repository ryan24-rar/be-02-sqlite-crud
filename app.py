from flask import Flask, jsonify, request

from postgres_repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    init_db,
    update_task,
)

app = Flask(__name__)

init_db()


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(get_all_tasks())


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def create_task_route():
    data = request.get_json()

    if data is None or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"].strip()

    if title == "":
        return jsonify({"error": "Title is required"}), 400

    new_task = create_task(title)

    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid request"}), 400

    existing_task = get_task_by_id(task_id)

    if existing_task is None:
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", existing_task["title"])
    done = data.get("done", existing_task["done"])

    if not isinstance(title, str) or title.strip() == "":
        return jsonify({"error": "Title is required"}), 400

    updated_task = update_task(
        task_id,
        title.strip(),
        bool(done)
    )

    return jsonify(updated_task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    deleted = delete_task(task_id)

    if not deleted:
        return jsonify({"error": "Task not found"}), 404

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)