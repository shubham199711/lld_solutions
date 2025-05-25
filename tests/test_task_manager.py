from datetime import datetime, timedelta
from unittest.mock import MagicMock
from apps.task_manager import User, DesignerTask, Project, NotificationService, TaskStatus, TaskFactory, TaskType

def test_assign_user_and_task():
    mock_notifier = MagicMock(spec=NotificationService)
    user = User("Test User", mock_notifier)
    task = DesignerTask("Test Task", datetime.now() + timedelta(days=1))
    project = Project("Test Project")

    project.add_user(user)
    project.add_task(task)
    project.assign_task(task, user)

    assert user in project.users
    assert task in project.tasks
    assert task in user.assigned_tasks
    assert user in task.assigned_to

def test_due_task_notification():
    mock_notifier = MagicMock(spec=NotificationService)
    user = User("Test User", mock_notifier)
    task = DesignerTask("Overdue Task", datetime.now() - timedelta(days=1))
    project = Project("Deadline Project")

    project.add_user(user)
    project.add_task(task)
    project.assign_task(task, user)

    project.due_date_notify()

    mock_notifier.notify.assert_called_with(user, "Task 'Overdue Task' is due!")

def test_update_status_threads():
    task = DesignerTask("Concurrent Task", datetime.now() + timedelta(days=1))
    assert task.status == TaskStatus.TODO
    task.update_status(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS

def test_verify_task_factory():
    task_factory = TaskFactory()
    task = task_factory.create_task(TaskType.DESIGN, "test", datetime.now() + timedelta(days=2))
    assert task.status == TaskStatus.TODO
    assert isinstance(task, DesignerTask)