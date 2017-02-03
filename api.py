from flask import Flask, request, render_template
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('todo-task')

todos = {
    'todo1': 'Save the world',
    'todo2': 'Floss'
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in todos:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        if todo_id not in todos:
            todos[todo_id] = request.form['task']
            return {todo_id: todos[todo_id]}, 201
        else:
            return {todo_id: todos[todo_id]}

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del todos[todo_id]
        return '', 204


class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(todos.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        if task in args:
            todos[todo_id] = args['task']
            return {todo_id: todos[todo_id]}, 201
        else:
            abort(400, "Missing 'task' form field")

api.add_resource(Todo, '/todos/<string:todo_id>')
api.add_resource(TodoList, '/todos')

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
