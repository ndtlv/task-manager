from flask import request
from flask_restful import Resource

from models import Dashboard, User, serialize_multiple, Task, Comment
from settings import db
from services import emit_object_creation


class TaskComments(Resource):
    def get(self, task_id):
        return serialize_multiple(
            db.session.query(Comment).filter(Comment.task_id == task_id)
        )

    def post(self, task_id):
        user_id = request.get_json()['user_id']
        dash_id = Task.query.get(task_id).dashboard_id
        if User.query.get(user_id) in Dashboard.query.get(dash_id).users:
            data = request.get_json()
            data.update({"task_id": task_id})
            com = Comment(**data)
            db.session.add(com)
            db.session.flush()
            id = com.id
            emit_object_creation({"name": com.body, "type": "comment"})
            db.session.commit()

            return {'id': id}, 201
        return "User cannot operate on this dashboard", 400
