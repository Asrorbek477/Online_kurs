from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from courses.models import Course
from payments.models import Payment
from users.permissions import IsInstructor
from .models import Student
from .serializers import StudentSerializer


class EnrollCourseView(APIView):
    """POST /api/courses/{course_id}/enroll/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)

        # Pullik kurs uchun to'lovni tekshirish
        if course.price > 0:
            has_paid = Payment.objects.filter(
                user=request.user,
                course=course,
                status='completed'
            ).exists()
            if not has_paid:
                return Response(
                    {'detail': "Avval to'lov qiling: /api/courses/{id}/pay/"},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Student profili olish yoki yaratish
        student, _ = Student.objects.get_or_create(user=request.user)

        # Allaqachon yozilganmi?
        if course in student.courses.all():
            return Response(
                {'detail': 'Siz bu kursga allaqachon yozilgansiz.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kursga yozish – bu yerda signal ishlaydi
        student.courses.add(course)

        return Response(
            {
                'message': f"'{course.title}' kursiga muvaffaqiyatli yozildingiz!",
                'student': StudentSerializer(student).data
            },
            status=status.HTTP_200_OK
        )


class CourseStudentsView(generics.ListAPIView):
    """GET /api/courses/{course_id}/students/ — Faqat instruktor"""
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])

        # Faqat kurs egasi ko'ra oladi
        if course.instructor != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Bu faqat kurs egasiga ko'rinadi.")

        return Student.objects.filter(courses=course).select_related('user')