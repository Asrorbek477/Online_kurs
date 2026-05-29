from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def validate(self, attrs):
        request = self.context['request']
        course_id = self.context['course_id']

        # Bir kursga ikki marta sharh qoldirib bo'lmaydi
        if Review.objects.filter(user=request.user, course_id=course_id).exists():
            raise serializers.ValidationError(
                {'detail': 'Siz bu kursga allaqachon sharh qoldirdingiz.'}
            )
        return attrs