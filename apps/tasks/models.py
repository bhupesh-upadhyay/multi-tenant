from django.db import models
from django.contrib.auth.models import User
from apps.common.models import SoftDeleteModel
from apps.projects.models import Project

# Create your models here.

class Task(SoftDeleteModel):
    STATUS_CHOICES = (
        ('TODO','TODO'),
        ('IN_PROGRESS','InProgress'),
        ('ON_HOLD','OnHold'),
        ('DONE','Done'),
    )
    PRIORITY_CHOICES = (
        ('HIGH', 'High'),
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium')
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tasks', null=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_tasks', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["project"]),
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
        ] 