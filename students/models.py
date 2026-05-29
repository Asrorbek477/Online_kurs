from django.db import models
from django.conf import settings
from courses.models import Course


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    courses = models.ManyToManyField(
        Course,
        related_name='enrolled_students',
        blank=True
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.user.username}"