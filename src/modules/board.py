from typing import List

from dbhandler import dbh
from task import Task


class Board:
    def __init__(self, name: str, label: str = ""):
        self.name = name
        self.label = label
        self.tasks: List[Task] = []
        self.id = dbh.create_board(name, label)

    def get_board_name(self) -> str:
        return self.name

    def get_board_label(self) -> str:
        return self.label

    def add_task(self, task: Task):
        task.id = dbh.create_task(self.id, task)
        self.tasks.append(task)

    # update_task_status returns true if status was updates, and false if task not found
    def update_task_status(self, task_name: str, new_status: str) -> bool:
        for task in self.tasks:
            if task.name == task_name:
                task.status = new_status
                dbh.update_task(task)
                return True

        return False

    def delete_task(self, task_name: str):
        dbh.delete_task(self.id, task_name)
        self.tasks = filter(lambda task: (
            task.task_name != task_name), self.tasks)

    def list_tasks(self):
        for task in self.tasks:
            print(
                f'{task.task_name} {task.status} {task.creation_date} {task.priority}')

    # print_task returns true if status was updates, and false if task not found
    def print_task(self, task_name: str):
        for task in self.tasks:
            if task.name == task_name:
                task.print_task()
                return

        print(f'Task {task_name} not found :(')
