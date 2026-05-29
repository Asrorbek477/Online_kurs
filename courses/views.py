from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer, CourseWriteSerializer
from .filters import CourseFilter
from users.permissions import IsInstructor
from django.db.models import Avg


class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/ — Hammaga ochiq
    POST /api/courses/ — Faqat instruktor
    """

    def get_queryset(self):  # ← bu metod qo'shiladi
        return Course.objects.select_related('instructor').annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-created_at')

    queryset = Course.objects.select_related('instructor').all()
    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'instructor__username']
    ordering_fields = ['price', 'created_at','avg_rating']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsInstructor()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseWriteSerializer
        return CourseSerializer


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET         — Hammaga ochiq
    PUT/PATCH   — Faqat kurs egasi instruktor
    DELETE      — Faqat kurs egasi instruktor
    """
    queryset = Course.objects.select_related('instructor').all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsInstructor()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CourseWriteSerializer
        return CourseSerializer

    def get_object(self):
        obj = super().get_object()
        # Faqat o'z kursini o'zgartira oladi
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.instructor != self.request.user:
                raise PermissionDenied("Siz faqat o'zingiz yaratgan kursni o'zgartira olasiz.")
        return obj