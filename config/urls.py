from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("lms/", include("lms.urls", namespace="lms")),
]
