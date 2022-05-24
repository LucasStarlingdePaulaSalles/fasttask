import unittest

from src.modules.dbhandler import DBHandler

class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.db = DBHandler()

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
        board = self.db.create_board(board_name = "test_board", board_label =
        "test")
        board_2 = self.db.create_board(board_name = "test_board_2", board_label =
        "test")

        boards = self.db.get_boards()
        self.assertTrue(len(boards) == 2)

        self.db.delete_board(board_id = board_2.get_board_id())
        boards = self.db.get_boards()
        self.assertTrue(len(boards) == 1)

    def test_create_task_in_board(self):
        pass

    def test_create_multiple_tasks_in_one_board(self):
        pass

    def test_create_multiple_tasks_in_two_board(self):
        pass

    def test_update_task(self):
        pass

    def test_delete_task(self):
        pass


