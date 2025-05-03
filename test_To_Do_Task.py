import unittest
import json
import os
from unittest.mock import patch
from To_Do_Task import load_tasks, save_tasks, add_task, mark_done, TASKS_FILE


class TestToDoTask(unittest.TestCase):

    def setUp(self):
        # Back up existing tasks file if it exists
        self.backup_file = TASKS_FILE + '.bak'
        if os.path.exists(TASKS_FILE):
            os.rename(TASKS_FILE, self.backup_file)
        # Ensure a clean slate by removing any lingering test file
        if os.path.exists(TASKS_FILE):
             os.remove(TASKS_FILE)

    def tearDown(self):
        # Remove the tasks file created during the test
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)
        # Restore the backup if it exists
        if os.path.exists(self.backup_file):
            os.rename(self.backup_file, TASKS_FILE)

    def test_load_tasks_no_file(self):
        # setUp ensures the file doesn't exist
        tasks = load_tasks()
        self.assertEqual(tasks, [])

    def test_load_tasks_existing_file(self):
        # Create a sample tasks file
        sample_tasks = [{'text': 'Test Task 1', 'done': False}, {'text': 'Test Task 2', 'done': True}]
        with open(TASKS_FILE, 'w') as f:
            json.dump(sample_tasks, f)

        tasks = load_tasks()
        self.assertEqual(tasks, sample_tasks)

    def test_save_tasks_empty_list(self):
        save_tasks([])
        # Check if file exists and contains an empty list
        self.assertTrue(os.path.exists(TASKS_FILE))
        with open(TASKS_FILE, 'r') as f:
            content = json.load(f)
        self.assertEqual(content, [])

    def test_save_tasks_with_data(self):
        sample_tasks = [{'text': 'Save Task 1', 'done': True}, {'text': 'Save Task 2', 'done': False}]
        save_tasks(sample_tasks)
        # Check if file exists and contains the sample data
        self.assertTrue(os.path.exists(TASKS_FILE))
        with open(TASKS_FILE, 'r') as f:
            content = json.load(f)
        self.assertEqual(content, sample_tasks)

    @patch('builtins.input', return_value='New Task 1')
    def test_add_task_to_empty_list(self, mock_input):
        tasks = []
        add_task(tasks)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['text'], 'New Task 1')
        self.assertFalse(tasks[0]['done'])

    @patch('builtins.input', return_value='New Task 2')
    def test_add_task_to_existing_list(self, mock_input):
        tasks = [{'text': 'Existing Task', 'done': True}]
        add_task(tasks)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['text'], 'Existing Task') # Verify original task is still there
        self.assertTrue(tasks[0]['done'])
        self.assertEqual(tasks[1]['text'], 'New Task 2') # Verify new task
        self.assertFalse(tasks[1]['done'])

    # Mock both input and print (as mark_done calls show_tasks)
    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_mark_done_valid_index(self, mock_print, mock_input):
        tasks = [{'text': 'Task to be done', 'done': False}]
        mark_done(tasks)
        self.assertTrue(tasks[0]['done'])

    @patch('builtins.input', return_value='99') # Invalid index
    @patch('builtins.print')
    def test_mark_done_invalid_index(self, mock_print, mock_input):
        tasks = [{'text': 'Task 1', 'done': False}, {'text': 'Task 2', 'done': False}]
        original_tasks = tasks.copy() # Keep a copy for comparison
        mark_done(tasks)
        # Verify the list hasn't changed for an invalid index
        self.assertEqual(tasks, original_tasks)

    # Add a test case for marking the second item done
    @patch('builtins.input', return_value='2')
    @patch('builtins.print')
    def test_mark_done_second_item(self, mock_print, mock_input):
        tasks = [{'text': 'Task 1', 'done': False}, {'text': 'Task 2', 'done': False}]
        mark_done(tasks)
        self.assertFalse(tasks[0]['done']) # First task should be unchanged
        self.assertTrue(tasks[1]['done']) # Second task should be done

# Add a main block to run the tests
if __name__ == '__main__':
    unittest.main()
