import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestRegister:

    def test_student_royxatdan_otadi(self, api_client):
        response = api_client.post(reverse('register'), {
            'username': 'student1', 'email': 'student@test.com',
            'password': 'Pass1234!', 'password2': 'Pass1234!',
            'is_instructor': False
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_instruktor_royxatdan_otadi(self, api_client):
        response = api_client.post(reverse('register'), {
            'username': 'ins1', 'email': 'ins@test.com',
            'password': 'Pass1234!', 'password2': 'Pass1234!',
            'is_instructor': True
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['is_instructor'] is True

    def test_parol_mos_kelmasa_xato(self, api_client):
        response = api_client.post(reverse('register'), {
            'username': 'u1', 'email': 'u@test.com',
            'password': 'Pass1234!', 'password2': 'Boshqa!'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestMyAccount:

    def test_oz_profilini_koradi(self, api_client):
        user = User.objects.create_user(
            username='me', email='me@test.com', password='Pass123!'
        )
        api_client.force_authenticate(user=user)
        response = api_client.get(reverse('my-account'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'me'

    def test_loginsiz_kira_olmaydi(self, api_client):
        response = api_client.get(reverse('my-account'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED