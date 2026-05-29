from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from courses.models import Course
from users.permissions import IsInstructor
from .models import Lesson
from .serializers import LessonSerializer, LessonWriteSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/{course_id}/lessons/
    POST /api/courses/{course_id}/lessons/ — Faqat kurs egasi instruktor
    """
    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsInstructor()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LessonWriteSerializer
        return LessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        # Faqat kurs egasi dars qo'sha oladi
        if course.instructor != self.request.user:
            raise PermissionDenied("Siz faqat o'z kursingizga dars qo'sha olasiz.")
        serializer.save(course=course)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/lessons/{id}/
    PUT    /api/lessons/{id}/ — Faqat kurs egasi
    DELETE /api/lessons/{id}/ — Faqat kurs egasi
    """
    queryset = Lesson.objects.select_related('course__instructor').all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsInstructor()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LessonWriteSerializer
        return LessonSerializer

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.course.instructor != self.request.user:
                raise PermissionDenied("Siz faqat o'z kurslaringizning darslarini o'zgartira olasiz.")
        return obj