from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('ico_bids.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
