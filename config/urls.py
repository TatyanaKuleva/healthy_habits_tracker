
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("tracker/", include("tracker.urls", namespace="tracker")),
    path("users/", include("users.urls", namespace="users")),
]
