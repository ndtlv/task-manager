from flask import request
from flask_restful import Resource

from models import Dashboard, User, Task
from utils.validator import ModelValidator
from settings import db
from services import emit_object_creation


class DashboardTasks(Resource):
    def get(self, dash_id):
        status = request.args.get('status')
        return ModelValidator(Task).get_dashboard_tasks(dash_id, status)

    def post(self, dash_id):
        dash = Dashboard.query.get(dash_id)
        user_id = request.get_json()["creator"]
        if User.query.get(user_id) in dash.users:
            data = request.get_json()
            data.update({"dashboard_id": dash_id})
            task = Task(**data)
            db.session.add(task)
            db.session.flush()
            id = task.id
            emit_object_creation({"name": dash.name, "type": "task"})
            dash.tasks.append(task)
            db.session.commit()

            return {"id": id}, 201
        return "User cannot operate on this dashboard", 400


class SingleTask(Resource):
    def get(self, task_id):
        return ModelValidator(Task).get_by_id(task_id)

    def patch(self, task_id):
        data = request.get_json()
        return ModelValidator(Task).patch_by_id(task_id, data)

    # assigning user to a specific task
    def post(self, task_id):
        user_id = request.get_json()['user_id']
        user = User.query.get(user_id)
        task = Task.query.get(task_id)
        dash = Dashboard.query.get(task.dashboard_id)
        if user in dash.users:
            task.users.append(user)
            db.session.commit()

            return {}, 201
        return "User cannot operate on this dashboard", 400
