from flask import Flask, request, send_from_directory, jsonify
import json, os, threading

app = Flask(__name__, static_folder='static')
DATA_FILE = 'tasks.json'
lock = threading.Lock()

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    with lock:
        tasks = load_tasks()
        if request.method == 'GET':
            return jsonify(tasks)
        data = request.get_json()
        if not data or not data.get('text'):
            return {'error': 'text required'}, 400
        task = {'id': int(os.times().elapsed * 1000), 'text': data['text'], 'done': False}
        tasks.append(task)
        save_tasks(tasks)
        return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task_ops(task_id):
    with lock:
        tasks = load_tasks()
        idx = next((i for i,t in enumerate(tasks) if t['id']==task_id), -1)
        if idx == -1: return '', 404
        if request.method == 'PUT':
            data = request.get_json()
            tasks[idx]['done'] = bool(data.get('done', tasks[idx]['done']))
            save_tasks(tasks)
            return jsonify(tasks[idx])
        else:  # DELETE
            tasks.pop(idx)
            save_tasks(tasks)
            return '', 204

if __name__ == '__main__':
    app.run(port=8000, debug=True)
