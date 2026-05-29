import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def instructor(db):
    return User.objects.create_user(
        username='instructor', email='i@test.com',
        password='Pass123!', is_instructor=True
    )

@pytest.fixture
def student(db):
    return User.objects.create_user(
        username='student', email='s@test.com',
        password='Pass123!', is_instructor=False
    )

@pytest.fixture
def course(db, instructor):
    return Course.objects.create(
        title='Django Basics', description='Kurs haqida',
        price=100000, instructor=instructor
    )


@pytest.mark.django_db
class TestCourseCreate:

    def test_instruktor_kurs_yaratadi(self, api_client, instructor):
        api_client.force_authenticate(user=instructor)
        url = reverse('course-list')
        data = {'title': 'Python', 'description': 'Test', 'price': 50000}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_student_kurs_yarata_olmaydi(self, api_client, student):
        api_client.force_authenticate(user=student)
        url = reverse('course-list')
        data = {'title': 'Python', 'description': 'Test', 'price': 0}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_loginsiz_kurs_yarata_olmaydi(self, api_client):
        url = reverse('course-list')
        response = api_client.post(url, {'title': 'X', 'description': 'Y', 'price': 0})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_narx_filtri_ishlaydi(self, api_client, course):
        url = reverse('course-list')
        response = api_client.get(url, {'min_price': 50000})
        assert response.status_code == status.HTTP_200_OK

    def test_boshqa_instruktor_kursni_ozgartira_olmaydi(self, api_client, course):
        other = User.objects.create_user(
            username='other', email='o@test.com',
            password='Pass123!', is_instructor=True
        )
        api_client.force_authenticate(user=other)
        url = reverse('course-detail', args=[course.id])
        response = api_client.patch(url, {'title': 'Hacked'})
        assert response.status_code == status.HTTP_403_FORBIDDEN