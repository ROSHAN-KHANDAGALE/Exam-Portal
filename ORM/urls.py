from django.urls import path
from . import views

# Create your Urls here
urlpatterns = [
    path("", views.Login.as_view(), name="index"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("forgot/", views.Forgot.as_view(), name="forgot"),
    path("reset/<uuid>", views.Reset.as_view(), name="reset"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("home/", views.Home.as_view(), name="home"),
    path("studentRegister/", views.StudentRegister.as_view(), name="studentRegister"),
    path("examForm/", views.Exam.as_view(), name="examForm"),
]
