
import json
import os

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

def show_tasks(tasks):
    if not tasks:
        print("No tasks.")
    for idx, task in enumerate(tasks, start=1):
        status = "✔" if task['done'] else "✗"
        print(f"{idx}. [{status}] {task['text']}")

def add_task(tasks):
    text = input("Enter new task: ")
    tasks.append({'text': text, 'done': False})
    print("Task added.")

def mark_done(tasks):
    show_tasks(tasks)
    idx = int(input("Enter task number to mark done: ")) - 1
    if 0 <= idx < len(tasks):
        tasks[idx]['done'] = True
        print("Task marked as done.")

def main():
    tasks = load_tasks()
    while True:
        print("\n1. View Tasks\n2. Add Task\n3. Mark Done\n4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            show_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
            save_tasks(tasks)
        elif choice == '3':
            mark_done(tasks)
            save_tasks(tasks)
        elif choice == '4':
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
