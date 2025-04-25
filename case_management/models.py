from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

TITLE_MAX_LENGTH = 64

class Task(models.Model):

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    slug = models.SlugField(unique=True, blank=True)
    due_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class TaskHistory(models.Model):

    STATUS_OPTIONS = {
        "U": "Unassigned",
        "A": "Active",
        "C": "Closed",
        "P": "Paused",
        "R": "Review pending"
    }

    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default="U")
    date_created = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='created_tasks')
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='assigned_tasks', null=True)

class TaskNote(models.Model):

    description = models.CharField()
    date_created = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
