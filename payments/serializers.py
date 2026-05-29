from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user_username', 'course', 'course_title',
            'amount', 'status', 'status_display', 'payment_date'
        ]
        read_only_fields = ['user', 'amount', 'status', 'payment_date']