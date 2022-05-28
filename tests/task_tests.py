import unittest
from src.modules.task import Task

class TestTask(unittest.TestCase):

    def test_update_status(self):
        task = Task(task_id=0, task_name="test_task", status="none",
                creation_date="", label="test", board_id="1", time_worked="0",
                priority=0)

        new_status = "todo"
        task.update_status(new_status)

        self.assertTrue(task.get_task_details()["status"] == "todo")


