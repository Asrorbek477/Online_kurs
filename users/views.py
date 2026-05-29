from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from .permissions import IsOwnerOrAdmin


class RegisterView(generics.CreateAPIView):
    """POST /api/register/ — Ro'yxatdan o'tish"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Token shart emas

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': "Ro'yxatdan muvaffaqiyatli o'tdingiz!",
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class UserListView(generics.ListAPIView):
    """GET /api/users/ — Barcha foydalanuvchilar (faqat admin)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE /api/users/{id}/"""
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


class MyAccountView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE /api/users/my-account/ — O'z akkauntim"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # pk shart emas – token orqali kim ekanini bilamiz
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer