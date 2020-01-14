from sqlalchemy.exc import InvalidRequestError
from settings import db
from models import Dashboard, Comment, Task, User, serialize_multiple


class ModelValidator:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, object_id):
        try:
            return self.model.query.get(object_id).serialize()
        except AttributeError:
            return "Not found", 404

    def patch_by_id(self, object_id, data):
        if "id" not in data.keys():
            try:
                db.session.query(self.model).filter_by(id=object_id).update(data)
            except InvalidRequestError:
                return {}, 400
            db.session.commit()
            return {}, 204
        return "id shouldn't be changed", 400

    @staticmethod
    def get_dashboard_tasks(dash_id, status):
        if status:
            return serialize_multiple(
                db.session.query(Task).filter_by(status=status)
            )
        return serialize_multiple(Dashboard.query.get(dash_id).tasks)