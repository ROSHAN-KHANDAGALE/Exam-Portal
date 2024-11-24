from django.urls import path
from . import views

# Create your Urls here
urlpatterns = [
    # Class based View
    path("", views.Login.as_view(), name="index"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("forgot/", views.Forgot.as_view(), name="forgot"),
    path("reset/<uuid>", views.Reset.as_view(), name="reset"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("home/", views.Home.as_view(), name="home"),
    path("studentRegister/", views.StudentRegister.as_view(), name="studentRegister"),
    # Generic View
    path("examForm/", views.ExamListView.as_view(), name="examForm"),
    path("examForm/create", views.ExamCreateView.as_view(), name="examForm_post"),
    path("subject/", views.SubjectListView.as_view(), name="subject"),
    path("subject/create", views.SubjectCreateView.as_view(), name="subject_post"),
    path("teacher/", views.TeacherListView.as_view(), name="teacher"),
    path("teacher/post", views.TeacherCreateView.as_view(), name="teacher_post"),
]
