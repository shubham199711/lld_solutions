from enum import Enum
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Notify(ABC):
    @abstractmethod
    def notify(self, message: str):
        raise NotImplementedError

class ConsoleNotify(Notify):
    def notify(self, message: str):
        print(message)

class User:
    def __init__(self, name: str, notify_method: Notify | None = None) -> None:
        self.name = name
        self.assigned_tasks: set[Task]  = set([])
        self.notify_method = notify_method or ConsoleNotify()

    def assigned_task(self, task: "Task"):
        self.assigned_tasks.add(task)
    
    def notify(self, message: str):
        self.notify_method.notify(message)



class Status(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    TODO = "TODO"
    DONE = "DONE"

class Task:
    def __init__(self, name: str, deadline: int) -> None:
        self.name = name
        self.assigned_user: set[User]  = set([])
        self.deadline = datetime.now() + timedelta(days=deadline)
        self.status = Status.TODO
    
    def assign_to(self, user: User):
        self.assigned_user.add(user)
        user.assigned_task(self)
    
    def change_status(self, status_update: Status):
        self.status = status_update
    
    def notifiy_users(self, message: str):
        for user in self.assigned_user:
            user.notify(message)
    
    def is_deadline(self, condition_fu = None) -> bool:
        if condition_fu is not None:
            return bool(condition_fu(self))
        if self.deadline.date() == datetime.now().date():
            return True
        return False

    def __repr__(self):
        return f"Task({self.name}, status={self.status.value}, deadline={self.deadline.date()})"


class Project:
    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks: set[Task] = set([])
    
    def add_task(self, task: Task):
        self.tasks.add(task)
    
    def notifiy_deadlines(self, deadline_fn = None):
        for task in self.tasks:
            if deadline_fn:
                if task.is_deadline(deadline_fn):
                    task.notifiy_users(f"Reminder: Task '{task.name}' in project '{self.name}' is due today!")
            else:
                if task.is_deadline():
                    task.notifiy_users(f"Reminder: Task '{task.name}' in project '{self.name}' is due today!")



if __name__ == "__main__":
    project = Project("test1")
    user1 = User("test_user1")
    task1 = Task("task1", 0)
    task1.assign_to(user1)
    project.add_task(task1)
    project.notifiy_deadlines()


    
