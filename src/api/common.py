from flask import Flask, jsonify
from src.database.common import execute
from src.database.queries import CREATE_TASK, INSPECT_TASK
from src.logger import LOGGER

app = Flask(__name__)


@app.route('/task/<int:task_id>')
def inspect_task(task_id):
    """ Return information about a task's status """
    task_row = execute(INSPECT_TASK, (task_id, ), logger=LOGGER)
    if not task_row:
        return jsonify('Task not found'), 404

    result = {
        'task_id': task_row['id'],
        'status': task_status(task_row)
    }
    return jsonify(result)


@app.route('/task/', methods=['POST'])
def create_task():
    """ Create a new task in the database and return its id """
    result = execute(CREATE_TASK, logger=LOGGER)
    task_id = result['id']
    return jsonify(task_id), 201, {'location': f'/task/{task_id}'}


def task_status(task_row):
    """ Determine whether a task has been finished, started or created """
    if task_row['exec_time']:
        return 'Completed'
    elif task_row['start_time']:
        return 'Run'
    else:
        return 'In Queue'
