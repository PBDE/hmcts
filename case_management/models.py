from django.db import models
from django.contrib.auth import get_user_model

class Task(models.Model):

    TITLE_MAX_LENGTH = 64

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    due_date = models.DateField()
    assigned_user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

class TaskHistory(models.Model):

    STATUS_OPTIONS = {
        "U": "Unassigned",
        "A": "Active",
        "C": "Closed",
        "P": "Paused",
        "R": "Review pending"
    }

    status = models.CharField(max_length=1, choices=STATUS_OPTIONS)
    date_created = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

class TaskNotes(models.Model):

    description = models.CharField()
    date_created = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
