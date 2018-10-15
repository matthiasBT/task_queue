from flask import Flask, jsonify

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
    task_id = 123456
    return jsonify(task_id), 201, {'location': '/task/{}'.format(task_id)}
