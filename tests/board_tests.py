import unittest
from src.modules.board import Board
from src.modules.task import Task

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(board_id=1, name="test_board", label="test")

    def test_add_task(self):
        task = Task(task_id=0, task_name="test_task", status="none",
                creation_date="", label="test", board_id="1", time_worked="0",
                priority=0)

        self.assertTrue(len(self.board.get_all_tasks()) == 0)

        self.board.add_task(task)

        self.assertTrue(len(self.board.get_all_tasks()) == 1)
        self.assertTrue(task in self.board.get_all_tasks())

    def test_update_task_status(self):
        task = Task(task_id=0, task_name="test_task", status="none",
                creation_date="", label="test", board_id="1", time_worked="0",
                priority=0)

        self.board.add_task(task)
        updated_task = self.board.update_task_status(task_name=task.name,
                new_status="todo")
        self.assertTrue(updated_task.status == "todo")

        updated_task = self.board.get_task(task_name=task.name)
        self.assertTrue(updated_task.status == "todo")

    def test_add_two_tasks_and_update_one(self):
        pass

    def test_delete_task(self):
        task = Task(task_id=0, task_name="test_task", status="none",
                creation_date="", label="test", board_id="1", time_worked="0",
                priority=0)

        self.board.add_task(task)

        self.board.delete_task(task_name=task.name)
        self.assertTrue(len(self.board.get_all_tasks()) == 0)

    def test_add_two_tasks_and_delete_one(self):
        pass
