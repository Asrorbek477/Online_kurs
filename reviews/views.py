from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from courses.models import Course
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from .throttles import ReviewRateThrottle


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/{course_id}/reviews/ — Hammaga ochiq
    POST /api/courses/{course_id}/reviews/ — Login qilgan foydalanuvchi
    """
    def get_queryset(self):
        return Review.objects.filter(
            course_id=self.kwargs['course_id']
        ).select_related('user')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_throttles(self):
        # Rate limiting faqat POST uchun
        if self.request.method == 'POST':
            return [ReviewRateThrottle()]
        return []

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['course_id'] = self.kwargs.get('course_id')  # Validatsiyada kerak
        return ctx

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(user=self.request.user, course=course)