from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from users.models import User


class Status(ChoiceEnum):
    BACKLOG = 'Backlog',
    IN_PROGRESS = 'InProgress',
    DONE = 'Done',



class Priority(ChoiceEnum):
    LOW = 'Low',
    MEDIUM = 'Medium',
    HIGH = 'High',
    CRITICAL = 'Critical',


class Task(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    assignee = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='assigneeTasks')
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='createdTasks')
    priority = EnumChoiceField(Priority, default=Priority.LOW, max_length=1)
    status = EnumChoiceField(Status, default=Status.BACKLOG, max_length=1)
    description = models.TextField(null=True, blank=True)

    @classmethod
    def update_status(task_id, status):
        task_id.status = status

    @classmethod
    def update_priority(task_id, priority):
        task_id.priority = priority


    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='comments')
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
