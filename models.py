from settings import db


users_dashboards_table = db.Table(
    "users_dashboards", db.Model.metadata,
    db.Column('user id', db.Integer, db.ForeignKey('users.id')),
    db.Column('dashboard id', db.Integer, db.ForeignKey('dashboards.id'))
    )


users_tasks_table = db.Table(
    "users_tasks", db.Model.metadata,
    db.Column('user id', db.Integer, db.ForeignKey('users.id')),
    db.Column('task id', db.Integer, db.ForeignKey('tasks.id'))
    )


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboards.id"))
    creator = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("User", secondary=users_tasks_table, backref="task")
    status = db.Column(db.String(15), nullable=False, default="To do")

    def __repr__(self):
        return f'Table: {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'dashboard id': self.dashboard_id,
            'creator': self.creator,
            'status': self.status
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    dashboards = db.relationship("Dashboard", secondary=users_dashboards_table,
                                 backref="user")
    tasks_created = db.relationship("Task")

    def __repr__(self):
        return f'User: {self.name}'

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name
        }


class Dashboard(db.Model):
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    tasks = db.relationship("Task", backref='dashboard')
    users = db.relationship("User", secondary=users_dashboards_table,
                            backref="dashboard")

    def __repr__(self):
        return f'Dashboard: {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    body = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Comment from {self.user_id}: {self.body}'

    def serialize(self):
        return {
            'id': self.id,
            'body': self.body,
            'user id': self.user_id,
            'task id': self.task_id
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


if __name__ == '__main__':
    db.create_all()
