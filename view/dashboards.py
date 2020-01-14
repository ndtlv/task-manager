from flask import request
from flask_restful import Resource

from models import Dashboard, serialize_multiple
from utils.validator import ModelValidator
from settings import db


class Dashboards(Resource):
    def get(self):
        return serialize_multiple(Dashboard.query.all())

    def post(self):
        data = request.get_json()
        user = Dashboard(**data)
        db.session.add(user)
        db.session.flush()
        id = user.id
        db.session.commit()

        return {'id': id}, 201


class SingleDashboard(Resource):
    def get(self, dash_id):
        return ModelValidator(Dashboard).get_by_id(dash_id)

    def patch(self, dash_id):
        data = request.get_json()
        return ModelValidator(Dashboard).patch_by_id(dash_id, data)

    def delete(self, dash_id):
        db.session.query(Dashboard).filter_by(id=dash_id).delete()
        db.session.commit()
        return 200
