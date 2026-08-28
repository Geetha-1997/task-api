"""
Task API — now backed by a real database via SQLAlchemy.

Endpoints:
  GET  /health          -> liveness/readiness probe (checks DB connectivity too)
  GET  /tasks            -> list all tasks
  POST /tasks            -> create a task {"title": "..."}
  GET  /tasks/<id>       -> get a single task
  DELETE /tasks/<id>     -> delete a task
"""

import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request, abort
from sqlalchemy import text

from db import SessionLocal, init_db, engine
from models import Task

app = Flask(__name__)

# Create tables on startup (idempotent — no-op if they already exist).
init_db()


def get_session():
    return SessionLocal()


@app.get("/health")
def health():
    """
    Liveness/readiness probe. Also verifies the database connection is
    alive — a health check that only pings the web process but not its
    dependencies can report 'healthy' while the app is actually unable
    to serve real requests.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        return jsonify(status="error", database="unreachable"), 503

    return jsonify(
        status="ok",
        database=db_status,
        time=datetime.now(timezone.utc).isoformat(),
    ), 200


@app.get("/tasks")
def list_tasks():
    session = get_session()
    try:
        tasks = session.query(Task).order_by(Task.id).all()
        return jsonify([t.to_dict() for t in tasks]), 200
    finally:
        session.close()


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        abort(400, description="'title' is required")

    session = get_session()
    try:
        task = Task(title=title)
        session.add(task)
        session.commit()
        session.refresh(task)
        return jsonify(task.to_dict()), 201
    finally:
        session.close()


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    session = get_session()
    try:
        task = session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found")
        return jsonify(task.to_dict()), 200
    finally:
        session.close()


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    session = get_session()
    try:
        task = session.get(Task, task_id)
        if not task:
            abort(404, description="Task not found")
        session.delete(task)
        session.commit()
        return "", 204
    finally:
        session.close()


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify(error=str(e.description)), e.code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
