from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'courses_count', 'joined_at']

    def get_courses_count(self, obj):
        return obj.courses.count()