from django.urls import path
from . import views

# Create your Urls here
urlpatterns = [
    # Class based View
    # Basic Login Operartions
    path("", views.Login.as_view(), name="index"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("forgot/", views.Forgot.as_view(), name="forgot"),
    path("reset/<uuid>", views.Reset.as_view(), name="reset"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("home/", views.Home.as_view(), name="home"),
    # operations
    path("studentRegister/", views.StudentRegister.as_view(), name="studentRegister"),
    path("settings/", views.Settings.as_view(), name="settings"),
    # Generic View (CRUD)
    # For Read
    path("examForm/", views.ExamListView.as_view(), name="examForm"),
    path("subject/", views.SubjectListView.as_view(), name="subject"),
    path("teacher/", views.TeacherListView.as_view(), name="teacher"),
    path(
        "subjectTeacher/", views.SubjectTeacherListView.as_view(), name="subjectTeacher"
    ),
    # For Create
    path("examForm/create", views.ExamCreateView.as_view(), name="examForm_post"),
    path("subject/create", views.SubjectCreateView.as_view(), name="subject_post"),
    path("teacher/create", views.TeacherCreateView.as_view(), name="teacher_post"),
    # For Update
    path(
        "student/update/<int:id>/",
        views.StudentUpdate.as_view(),
        name="student_update",
    ),
    # For Delete
    path(
        "student/delete/<int:id>/",
        views.StudentDelete.as_view(),
        name="student_delete",
    ),
]
