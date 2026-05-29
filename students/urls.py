from django.urls import path
from .views import EnrollCourseView, CourseStudentsView

urlpatterns = [
    path('courses/<int:course_id>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('courses/<int:course_id>/students/', CourseStudentsView.as_view(), name='course-students'),
]