from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/task/<int:task_id>')
def hello(task_id):
    result = {
        'task_id': task_id,
        'status': 'In Queue'
    }
    return jsonify(result)
