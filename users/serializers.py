from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Ro'yxatdan o'tish uchun."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Parolni tasdiqlang')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'is_instructor']

    def validate(self, attrs):
        # Ikkala parol mos kelishi kerak
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': 'Parollar mos kelmadi.'})
        return attrs

    def create(self, validated_data):
        # create_user – parolni hash qilib saqlaydi
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Foydalanuvchi ma'lumotlarini ko'rsatish uchun."""
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_instructor', 'role', 'date_joined']
        read_only_fields = ['date_joined']

    def get_role(self, obj):
        return 'Instruktor' if obj.is_instructor else 'Student'


class UserUpdateSerializer(serializers.ModelSerializer):
    """Profilni yangilash uchun – faqat ruxsat etilgan maydonlar."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']