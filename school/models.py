# models.py
from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=120, blank=True)
    subject_specialty = models.CharField(max_length=120, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class ClassSchedule(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=255)
    total_students = models.PositiveIntegerField(default=0)
    present_students = models.PositiveIntegerField(default=0)
    syllabus_coverage = models.PositiveIntegerField(default=0, help_text="Percentage of coverage for this session")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date", "-start_time")

    @property
    def absent_students(self):
        return max(self.total_students - self.present_students, 0)

    def __str__(self):
        return f"{self.class_name} - {self.topic}"


class Homework(models.Model):
    STATUS_CHOICES = (
        ("assigned", "Assigned"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    )

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=120)
    class_name = models.CharField(max_length=120)
    description = models.TextField()
    assigned_on = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="assigned")
    completed_count = models.PositiveIntegerField(default=0)
    pending_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("due_date",)

    def __str__(self):
        return self.title
