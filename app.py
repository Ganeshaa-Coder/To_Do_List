from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return []
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading tasks: {e}")
        return []


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")


@app.route('/')
def index():
    tasks = load_tasks()
    # Enumerate tasks for display, starting from 1
    enumerated_tasks = list(enumerate(tasks, 1))
    return render_template('index.html', tasks=enumerated_tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        tasks = load_tasks()
        tasks.append({'text': task_text, 'done': False})
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/done/<int:task_index>')
def done_task(task_index):
    tasks = load_tasks()
    # Adjust index to be 0-based for list access
    actual_index = task_index - 1
    if 0 <= actual_index < len(tasks):
        tasks[actual_index]['done'] = True
        save_tasks(tasks)
    else:
        # Handle invalid index, maybe flash a message later
        print(f"Invalid task index: {task_index}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
