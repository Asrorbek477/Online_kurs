from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger sozlash
schema_view = get_schema_view(
    openapi.Info(
        title="Online Kurs Platformasi API",
        default_version='v1',
        description="Kurslar, darslar, to'lovlar va ko'proq.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT tokenlar
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Applarning URL'lari
    path('api/', include('users.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('lessons.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('students.urls')),
    path('api/', include('reviews.urls')),

    # Swagger hujjatlari
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]