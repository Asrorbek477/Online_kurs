import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from courses.models import Course
from payments.models import Payment

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def instructor(db):
    return User.objects.create_user(
        username='ins', email='ins@test.com',
        password='Pass123!', is_instructor=True
    )

@pytest.fixture
def student(db):
    return User.objects.create_user(
        username='stu', email='stu@test.com',
        password='Pass123!', is_instructor=False
    )

@pytest.fixture
def course(db, instructor):
    return Course.objects.create(
        title='Kurs', description='Tavsif',
        price=100000, instructor=instructor
    )

@pytest.mark.django_db
class TestPayment:

    def test_tolov_muvaffaqiyatli(self, api_client, student, course):
        api_client.force_authenticate(user=student)
        response = api_client.post(reverse('course-pay', args=[course.id]))
        assert response.status_code == status.HTTP_201_CREATED
        assert Payment.objects.filter(
            user=student, course=course, status='completed'
        ).exists()

    def test_ikki_marta_tolov_bolmaydi(self, api_client, student, course):
        Payment.objects.create(
            user=student, course=course,
            amount=course.price, status='completed'
        )
        api_client.force_authenticate(user=student)
        response = api_client.post(reverse('course-pay', args=[course.id]))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_oz_tolovlarini_koradi(self, api_client, student, course):
        Payment.objects.create(
            user=student, course=course,
            amount=course.price, status='completed'
        )
        api_client.force_authenticate(user=student)
        response = api_client.get(reverse('payment-list'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1