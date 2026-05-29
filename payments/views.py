from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Course
from .models import Payment
from .serializers import PaymentSerializer


class PayCourseView(APIView):
    """POST /api/courses/{course_id}/pay/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)

        # Allaqachon to'lov qilinganmi?
        already_paid = Payment.objects.filter(
            user=request.user,
            course=course,
            status='completed'
        ).exists()

        if already_paid:
            return Response(
                {'detail': 'Siz bu kursni allaqachon sotib olgansiz.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # To'lovni yaratamiz (real loyihada payment gateway bo'ladi)
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            status='completed'
        )

        # O'quvchiga "Xush kelibsiz!" email
        send_mail(
            subject=f"🎉 {course.title} kursini sotib oldingiz!",
            message=(
                f"Assalomu alaykum, {request.user.username}!\n\n"
                f"'{course.title}' kursini muvaffaqiyatli sotib oldingiz.\n"
                f"Endi kursga yozilishingiz va darslarni boshlashingiz mumkin!\n\n"
                f"Muvaffaqiyatlar! 🚀"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

        return Response(
            {
                'message': "To'lov muvaffaqiyatli! Endi kursga yozilishingiz mumkin.",
                'payment': PaymentSerializer(payment).data
            },
            status=status.HTTP_201_CREATED
        )


class PaymentListView(generics.ListAPIView):
    """GET /api/payments/ — O'zim qilgan to'lovlar"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Faqat o'zining to'lovlari
        return Payment.objects.filter(user=self.request.user)