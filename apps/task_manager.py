from abc import ABC, abstractmethod
from enum import Enum
from threading import Lock
from datetime import datetime, timedelta


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskType(Enum):
    DESIGN = "design"
    FRONT_END = "front-end"
    BACK_END = "back-end"


class Task(ABC):
    def __init__(self, name: str, due_date: datetime):
        self.name = name
        self.due_date = due_date

    @abstractmethod
    def assign_to(self, user: "User"):
        pass

    @abstractmethod
    def update_status(self, status: TaskStatus):
        pass

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def is_due(self) -> bool:
        return False


class NotificationService(ABC):
    @abstractmethod
    def notify(self, user: "User", message: str):
        pass


class ConsoleNotificationService(NotificationService):
    def notify(self, user: "User", message: str):
        print(f"Notify {user.name}: {message}")


class User:
    def __init__(self, name: str, notification_strategy: NotificationService):
        self.name = name
        self.assigned_tasks = []
        self.notification_strategy = notification_strategy

    def assign_to(self, task: Task):
        if task not in self.assigned_tasks:
            self.assigned_tasks.append(task)

    def notify(self, message: str = "You have a task update"):
        self.notification_strategy.notify(self, message)


class DesignerTask(Task):
    def __init__(self, name: str, due_date: datetime):
        super().__init__(name, due_date)
        self.status = TaskStatus.TODO
        self.assigned_to = []
        self.lock = Lock()

    def assign_to(self, user: User):
        if user not in self.assigned_to:
            self.assigned_to.append(user)

    def update_status(self, status: TaskStatus):
        with self.lock:
            self.status = status

    def notify(self):
        for user in self.assigned_to:
            user.notify(f"Task '{self.name}' is due!")

    def is_due(self) -> bool:
        if self.due_date <= datetime.now():
            return True
        return False


class Project:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        self.tasks: list[Task] = []
        self.users: list[User] = []

    def add_user(self, user: User):
        if user not in self.users:
            self.users.append(user)

    def add_task(self, task: Task):
        if task not in self.tasks:
            self.tasks.append(task)

    def assign_task(self, task: Task, user: User):
        if task not in self.tasks:
            raise ValueError("Task not present in project")
        if user not in self.users:
            raise ValueError("User not present in project")
        task.assign_to(user)
        user.assign_to(task)

    def due_date_notify(self):
        for task in self.tasks:
            if task.is_due():
                task.notify()


class TaskFactory:
    def create_task(self, task_type: TaskType, task_name: str, task_due_date: datetime):
        if task_type == TaskType.DESIGN:
            return DesignerTask(task_name, task_due_date)
        raise ValueError("Other task type are not supported yet!")


if __name__ == "__main__":
    project = Project("Website Launch")
    task_factory = TaskFactory()
    task = task_factory.create_task(
        TaskType.DESIGN, "design website layout", datetime.now() - timedelta(days=1)
    )
    user = User("Designer User 1", ConsoleNotificationService())
    project.add_task(task)
    project.add_user(user)
    project.assign_task(user=user, task=task)
    project.due_date_notify()
