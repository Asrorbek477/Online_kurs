from django.urls import path
from .views import ReviewListCreateView

urlpatterns = [
    path('courses/<int:course_id>/reviews/', ReviewListCreateView.as_view(), name='course-reviews'),
]