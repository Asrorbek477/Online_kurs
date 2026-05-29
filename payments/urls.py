from django.urls import path
from .views import PayCourseView, PaymentListView

urlpatterns = [
    path('courses/<int:course_id>/pay/', PayCourseView.as_view(), name='course-pay'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]