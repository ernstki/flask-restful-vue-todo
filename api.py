import os
import sys
import click
import logging

from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

mypath = os.path.dirname(__file__)

putparser = reqparse.RequestParser(trim=True)
putparser.add_argument('task')

postparser = reqparse.RequestParser(trim=True)
postparser.add_argument('batch', type=list, location='json')

DEFAULT_TODOS = [
    { 'task': 'water the cactus', 'done': False },
    { 'task': 'heal the world', 'done': False },
    { 'task': 'floss', 'done': True }
]
SQLITE_DB = 'todos.db'

app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
    EXPLAIN_TEMPLATE_LOADING=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + SQLITE_DB,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(40))
    done = db.Column(db.Boolean) #, server_default=False) <-- didn't work

    def __init__(self, task, done=False):
        self.task = task
        self.done = done

    def __repr__(self):
        short = self.task[0:16] + ('...' if len(self.task) > 16 else '')
        if not self.id:
            return "<Todo task:'%s'>" % short
        else:
            return "<Todo id:%i, task:'%s'>" % (self.id, short)

    def as_dict(self):
        """
        Return this record as a dictionary
        """
        return { 'id': self.id, 'task': self.task, 'done': self.done }


def init_db():
    """
    Re-recreate all database tables and fill with sample data
    """
    db.drop_all()  # won't hurt anything if it doesn't exist
    db.create_all()
    for todo in DEFAULT_TODOS:
        t = Todo(todo['task'], todo['done'])
        click.secho('Adding ' + repr(t), fg='yellow')
        db.session.add(t)
    db.session.commit()


class TodoResource(Resource):
    def get(self, id):
        """
        Fetch an individual to-do by ID
        """
        t = Todo.query.get(id)
        if not t:
            abort(404, message="To-do {} doesn't exist" % id)
        return jsonify(Todo.query.get(id).as_dict())

    def put(self, id):
        """
        Update properties for an existing ID
        """
        try:
            args = putparser.parse_args(strict=True)
        except ValueError as e:
            logging.error(str(e))
            abort(400, message='This endpoint expects a single JSON object, '
                               'not an array')

        t = Todo.query.get(id)
        if not t:
            abort(404, message="To-do {} doesn't exist" % id)
        t.task = args['task']
        db.session.add(t)
        db.session.commit()
        return jsonify(t.as_dict())

    def delete(self, id):
        del todos[todo_id]
        t = Todo.query.get(id)
        if not t:
            abort(404, message="To-do {} doesn't exist" % id)
        db.session.delete(id)
        db.session.commit()
        return '', 204


class TodoListResource(Resource):
    def get(self):
        return jsonify([t.as_dict() for t in Todo.query.all()])

    def put(self):
        try:
            args = putparser.parse_args(strict=True)
        except ValueError as e:
            logging.error(str(e))
            abort(400, message='This endpoint expects a single JSON object, '
                               'not an array')
        t = Todo(args['task'])
        db.session.add(t)
        db.session.commit()
        return jsonify(t.as_dict())

    def post(self):
        if not request.is_json:
            abort(400, message="Endpoint expects Content-Type: application/json")

        logging.info(str(request.get_json()))
        args = postparser.parse_args(strict=True)
        todos = []

        for todo in args['batch']:
            logging.info('Added: %s' % repr(todo))
            t = Todo(todo['task'])
            db.session.add(t)
            todos.append(t)  # have to wait until commit before they get IDs

        db.session.commit()
        return jsonify([todo.as_dict() for todo in todos])


api.add_resource(TodoResource, '/todos/<int:id>')
api.add_resource(TodoListResource, '/todos')


@app.route('/')
def index():
    return render_template("index.html")


@app.before_first_request
def first_launch_init_db():
    if os.path.isfile(mypath + os.sep + SQLITE_DB):
        logging.info("Database '%s' already exists" % SQLITE_DB)
        return

    # otherwise, create the tables
    logging.info("Creating database '%s'" % SQLITE_DB)
    init_db()


@app.cli.command(name='initdb')
@click.option('--drop', is_flag=True, default=False,
              help='Delete existing datbase w/out prompting.')
def create_db_if_not_exist(drop, nonintr=False):
    """
    Create the database for the to-do list API
    """
    if os.path.isfile(mypath + os.sep + SQLITE_DB) and not drop:
        click.confirm(
            "Database exists. Really drop table(s) and re-create them?",
            abort=True)
        init_db()
    else:
        init_db()


if __name__ == '__main__':
    # You could specify host= and port= params here, but they won't be used if
    # you invoke the app in the usualy way with 'flask run'
    # Ref: http://flask.pocoo.org/docs/0.11/api/#flask.Flask.run
    #app.run(debug=True)
    click.secho('\nPlease launch the demo API with\n', err=True)
    click.secho('    export FLASK_APP=api.py', bold=True,
                err=True)
    click.secho('    flask run [--host=X.X.X.X] [--port=YYYY]\n', bold=True,
                err=True)
    sys.exit(1)
