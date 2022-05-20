class Task:
    def __init__(self, task_id, task_name, status, creation_date, label,
            board_id, time_worked=0, priority=0):
        self.task_id       = task_id
        self.task_name     = task_name
        self.status        = status
        self.creation_date = creation_date
        self.label         = label
        self.board_id      = board_id
        self.time_worked   = time_worked
        self.priority      = priority

    def print_task(self):
        print("Task details")
        print("Name: ", self.task_name)
        print("Status: ", self.status)
        print("Creation date: ", self.creation_date)
        print("Label: ", self.label)
        print("Priority: ", self.priority)
        print("Time Worked in this task: ", self.time_worked, "\n")

        return

    def start_working(self):
        pass

    def stop_working(self):
        pass

