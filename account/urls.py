from django.urls import path

from . import views

urlpatterns = [
    path("async-csrf/", views.get_async_csrf_token),
    path("api/account/login/", views.LoginView.as_view()),
    path("api/account/create/", views.ReplicaUserCreateAPIView.as_view()),
]
