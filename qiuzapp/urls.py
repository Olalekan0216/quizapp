from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quiz", views.quiz, name="quiz"),
    path("results", views.results, name="results"),
    path("auth/login", views.login, name="login"),
    path("auth/register", views.register, name="register"),
    path("auth/verify", views.verify, name="verify"),
    path("auth/logout", views.logout, name="logout"),
]