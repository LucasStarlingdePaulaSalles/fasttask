import unittest
import os
from src.modules.dbhandler import DBHandler

class TestDBHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_file = os.path.expanduser('~') + '/.fasttaskdb'
        if os.path.exists(cls.db_file):
            os.remove(cls.db_file)
        cls.db = DBHandler()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_file):
            os.remove(cls.db_file)

    def test_initialize_db(self):
        boards = self.db.get_boards()
        self.assertEqual(len(boards), 0)
        self.assertTrue(os.path.exists(os.path.expanduser('~') + '/.fasttaskdb'))

    def test_create_board(self):
        board = self.db.create_board(board_name = "test_board", board_label =
        "test")

        self.assertTrue(board.get_board_name() == "test_board")
        self.assertTrue(board.get_board_label() == "test")
        self.assertTrue(len(board.get_all_tasks()) == 0)

        #Tear Down
        sql = 'delete from boards where id = ?'
        params = (board.get_board_id(),)
        self.db.cur.execute(sql, params)
        self.db.conn.commit()

    def test_delete_board(self):
        board = self.db.create_board(board_name = "test_board", board_label =
        "test")
        board_2 = self.db.create_board(board_name = "test_board_2", board_label =
        "test")

        boards = self.db.get_boards()
        self.assertEqual(len(boards), 2)

        self.db.delete_board(board_id = board.get_board_id())
        boards = self.db.get_boards()
        self.assertEqual(len(boards), 1)

        self.db.delete_board(board_id = board_2.get_board_id())
        boards = self.db.get_boards()
        self.assertEqual(len(boards), 0)


    def test_create_task_in_board(self):
        board = self.db.create_board(board_name = "test_board", board_label =
        "test")
        task_name = 'TestTask'
        task_label = 'test'
        task_priority = 10
        task = self.db.create_task(board.get_board_id(), task_name,label=task_label, priority=task_priority)

        sql = """select
            id,
            name,
            label,
            priority,
            board_id
            from tasks where id = ?"""
        params = (task.id,)
        self.db.cur.execute(sql, params)
        task_data = self.db.cur.fetchall()[0]
        self.assertEqual(task_name, task_data[1])
        self.assertEqual(task_label, task_data[2])
        self.assertEqual(task_priority, task_data[3])
        self.assertEqual(board.get_board_id(), task_data[4])

        #Tear Down
        sql = 'delete from tasks where id = ?'
        params = (task.id,)
        self.db.cur.execute(sql, params)
        self.db.conn.commit()
        sql = 'delete from boards where id = ?'
        params = (board.get_board_id(),)
        self.db.cur.execute(sql, params)
        self.db.conn.commit()


    def test_delete_task(self):
        board = self.db.create_board(board_name = "test_board", board_label =
        "test")
        task_name = 'TestTask'
        task = self.db.create_task(board.get_board_id(), task_name)
        self.db.delete_task(task_id=task.id)
        sql = """select
            id,
            name,
            label,
            priority,
            board_id
            from tasks where id = ?"""
        params = (task.id,)
        self.db.cur.execute(sql, params)
        task_data = self.db.cur.fetchall()
        self.assertEqual(len(task_data),0)

        #Tear Down
        sql = 'delete from boards where id = ?'
        params = (board.get_board_id(),)
        self.db.cur.execute(sql, params)
        self.db.conn.commit()





