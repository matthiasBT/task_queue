from flask import Flask, jsonify
from database.common import execute
from database.queries import CREATE_TASK

app = Flask(__name__)


@app.route('/task/<int:task_id>')
def hello(task_id):
    result = {
        'task_id': task_id,
        'status': 'In Queue'
    }
    return jsonify(result)


@app.route('/task/', methods=['POST'])
def create_task():
    """ Create a new task in the database and return its id """
    result = execute(CREATE_TASK)
    task_id = result['id']
    return jsonify(task_id), 201, {'location': f'/task/{task_id}'}
