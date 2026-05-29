import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from courses.models import Course
from payments.models import Payment
from students.models import Student

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
def free_course(db, instructor):
    return Course.objects.create(
        title='Bepul', description='Desc',
        price=0, instructor=instructor
    )

@pytest.fixture
def paid_course(db, instructor):
    return Course.objects.create(
        title='Pullik', description='Desc',
        price=100000, instructor=instructor
    )

@pytest.mark.django_db
class TestEnrollment:

    def test_bepul_kursga_yoziladi(self, api_client, student, free_course):
        api_client.force_authenticate(user=student)
        response = api_client.post(reverse('course-enroll', args=[free_course.id]))
        assert response.status_code == status.HTTP_200_OK
        assert free_course in Student.objects.get(user=student).courses.all()

    def test_tolovsiz_pullik_kursga_yozilmaydi(self, api_client, student, paid_course):
        api_client.force_authenticate(user=student)
        response = api_client.post(reverse('course-enroll', args=[paid_course.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_tolovdan_keyin_yoziladi(self, api_client, student, paid_course):
        Payment.objects.create(
            user=student, course=paid_course,
            amount=paid_course.price, status='completed'
        )
        api_client.force_authenticate(user=student)
        response = api_client.post(reverse('course-enroll', args=[paid_course.id]))
        assert response.status_code == status.HTTP_200_OK

    def test_ikki_marta_yozilmaydi(self, api_client, student, free_course):
        s, _ = Student.objects.get_or_create(user=student)
        s.courses.add(free_course)
        api_client.force_authenticate(user=student)
        response = api_client.post(reverse('course-enroll', args=[free_course.id]))
        assert response.status_code == status.HTTP_400_BAD_REQUEST