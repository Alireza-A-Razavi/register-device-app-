from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.SignUpTempView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("async-csrf/", views.get_async_csrf_token),
]
