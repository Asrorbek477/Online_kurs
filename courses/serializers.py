from rest_framework import serializers
from .models import Course
from users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    """Ko'rsatish uchun – barcha ma'lumotlar."""
    avg_rating = serializers.FloatField(read_only=True)
    instructor = UserSerializer(read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    is_free = serializers.BooleanField(read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'price', 'is_free',
            'instructor', 'avg_rating', 'students_count',
            'lessons_count', 'created_at'
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseWriteSerializer(serializers.ModelSerializer):
    """Yaratish va yangilash uchun – instruktor o'zi belgilanadi."""
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price']

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)