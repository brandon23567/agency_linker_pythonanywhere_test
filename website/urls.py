from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/authentication/", include("authentication.urls")),
    path("api/agency_side/", include("agency_side.urls")),
    path("api/agency_client_side/", include("agency_client_side.urls")),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
