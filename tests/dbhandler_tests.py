import unittest

from src.modules.dbhandler import DBHandler

class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.db = DBHandler()
        boardTest = self.db.create_board(board_name = "test_boardTest", board_label =
        "test")

    def test_initialize_db(self):
        pass

    def test_create_board(self):
        boards = self.db.get_boards()
        self.assertTrue(len(boards) == 0)

        board = self.db.create_board(board_name = "test_board", board_label =
        "test")

        self.assertTrue(board.get_board_name() == "test_board")
        self.assertTrue(board.get_board_label() == "test")
        self.assertTrue(len(board.get_all_tasks()) == 0)

    def test_delete_board(self):
        boardsCount = len( self.db.get_boards())

        board_2 = self.db.create_board(board_name = "test_board_2", board_label =
        "test")

        boards = self.db.get_boards()

        self.assertTrue(len(boards) == boardsCount + 1)

        self.db.delete_board(board_id = board_2.board_id)
        boards = self.db.get_boards()
        self.assertTrue(len(boards) == boardsCount)

    def test_create_task_in_board(self):
        board_3 = self.db.create_board(board_name = "test_board_3", board_label =
        "test")

        task = self.db.create_task(board_id = board_3.board_id, task_name = "task", label = "teste", priority= 0)
        board_3.add_task(task)

        self.assertTrue(self.db.get_task(task).board_id == board_3.board_id)

    def test_create_multiple_tasks_in_board(self):
        board_4 = self.db.create_board(board_name = "test_board_4", board_label =
        "test")

        task1 = self.db.create_task(board_id = board_4.board_id, task_name = "task1", label = "teste", priority= 0)
        task2 = self.db.create_task(board_id = board_4.board_id, task_name = "task2", label = "teste", priority= 0)
        task3 = self.db.create_task(board_id = board_4.board_id, task_name = "task3", label = "teste", priority= 0)
        board_4.add_task(task1)
        board_4.add_task(task2)
        board_4.add_task(task3)

        self.assertTrue(self.db.get_board(len(board_4.board_id.tasks) == 3))

    def test_create_multiple_tasks_in_two_board(self):
        board_5 = self.db.create_board(board_name = "test_board_5", board_label =
        "test")
        board_6 = self.db.create_board(board_name = "test_board_6", board_label =
        "test")

        task1 = self.db.create_task(board_id = board_5.board_id, task_name = "task1", label = "teste", priority= 0)
        task2 = self.db.create_task(board_id = board_5.board_id, task_name = "task2", label = "teste", priority= 0)
        task3 = self.db.create_task(board_id = board_6.board_id, task_name = "task3", label = "teste", priority= 0)

        board_5.add_task(task1)
        board_5.add_task(task2)
        board_6.add_task(task3)

        self.assertTrue(self.db.get_board(len(board_5.board_id.tasks) == 2))
        self.assertTrue(self.db.get_board(len(board_6.board_id.tasks) == 1))

    def test_update_task(self):
        board_7 = self.db.create_board(board_name = "test_board_7", board_label =
        "test")

        task = self.db.create_task(board_id = board_7.board_id, task_name = "task1", label = "teste", priority= 0)
        board_7.add_task(task)

        assertTrue(self.db.update_task(task_id= task, new_status= "doing"))

    def test_delete_task(self):
        board_8 = self.db.create_board(board_name = "test_board_8", board_label =
        "test")

        task = self.db.create_task(board_id = board_8.board_id, task_name = "task1", label = "teste", priority= 0)
        board_8.add_task(task)

        assertTrue(self.db.delete_task(task_id= task))


