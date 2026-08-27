"""
Simple Task API — built as a portfolio project to demonstrate
containerization and multi-cloud deployment readiness.

Endpoints:
  GET  /health          -> liveness/readiness probe (used by Docker/K8s)
  GET  /tasks            -> list all tasks
  POST /tasks            -> create a task {"title": "..."}
  GET  /tasks/<id>       -> get a single task
  DELETE /tasks/<id>     -> delete a task
"""

import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory store (fine for a demo project — swap for a real DB in prod)
tasks = {}
next_id = 1


@app.get("/health")
def health():
    """Used by Docker HEALTHCHECK and would be used by a Kubernetes probe."""
    return jsonify(status="ok", time=datetime.now(timezone.utc).isoformat()), 200


@app.get("/tasks")
def list_tasks():
    return jsonify(list(tasks.values())), 200


@app.post("/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        abort(400, description="'title' is required")

    task = {
        "id": next_id,
        "title": title,
        "done": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    tasks[next_id] = task
    next_id += 1
    return jsonify(task), 201


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        abort(404, description="Task not found")
    return jsonify(task), 200


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if task_id not in tasks:
        abort(404, description="Task not found")
    del tasks[task_id]
    return "", 204


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify(error=str(e.description)), e.code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
