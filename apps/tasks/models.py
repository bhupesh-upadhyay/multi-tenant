from django.db import models
from django.contrib.auth.models import User
from common.models import SoftDeleteModel
from projects.models import Project

# Create your models here.

class Task(SoftDeleteModel):
    STATUS_CHOICE = (
        ('IN-PROGRESS','InProgress'),
        ('ON-HOLD','OnHold'),
        ('DONE','Done'),
        ('TODO','TODO'),
    )
    PRIORITY_CHOICES = (
        ('HIGHT', 'High'),
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium')
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default='TODO')
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES, default='LOW')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_task')
    due_date = models.DateField()
    
    class Meta:
        pass
        # unique_together = ("project", "title")