from time import sleep
from settings import app, api
import os

from view.users import DashboardUsers, SingleUser, Users
from view.dashboards import Dashboards, SingleDashboard
from view.tasks import DashboardTasks, SingleTask
from view.comments import TaskComments

api.add_resource(Users, '/users')
api.add_resource(DashboardUsers, '/dashboards/<int:dash_id>/users')
api.add_resource(SingleUser, '/users/<int:user_id>')

api.add_resource(Dashboards, '/dashboards')
api.add_resource(SingleDashboard, '/dashboards/<int:dash_id>')

api.add_resource(DashboardTasks, '/dashboards/<int:dash_id>/tasks')
api.add_resource(SingleTask, '/tasks/<int:task_id>')

api.add_resource(TaskComments, '/tasks/<int:task_id>/comments')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
