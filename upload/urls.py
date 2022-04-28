from django.urls import path

from . import views
app_name = 'upload'
urlpatterns = [
    path("", views.uploadFile, name = "uploadFile"),
    path("detail/", views.detail, name = "detail"),
    path("detail/download", views.download, name = "download")
]