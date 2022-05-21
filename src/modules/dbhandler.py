from src.modules.task import Task


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBHandler(metaclass=Singleton):
    def __init__(self) -> None:
        pass

    def get_connection(self):
        return self

    def create_board(self, board_name: str, board_label: str) -> int:
        pass

    def create_task(self, board_id: int, task: Task) -> int:
        pass

    def update_task(self, task: Task):
        pass

    def delete_task(self, board_id: int, task_name: str):
        pass


dbh = DBHandler()
