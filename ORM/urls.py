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
    # For Subject (CRUD) [DONE]
    path("subject/", views.SubjectListView.as_view(), name="subject"),
    path("subject/create", views.SubjectCreateView.as_view(), name="subject_post"),
    path(
        "student/update/<int:id>/",
        views.StudentUpdate.as_view(),
        name="student_update",
    ),
    path(
        "student/delete/<int:id>/",
        views.StudentDelete.as_view(),
        name="student_delete",
    ),
    
    
    # For Exam (CR) [DONE]
    path("examForm/", views.ExamListView.as_view(), name="exam"),
    path("examForm/create", views.ExamCreateView.as_view(), name="examForm_post"),
    
    
    # For Teacher (CRUD) [DONE]
    path("teacher/", views.TeacherListView.as_view(), name="teacher"),
    path("teacher/create", views.TeacherCreateView.as_view(), name="teacher_post"),
    path(
        "teacher/update/<int:pk>/",
        views.TeacherUpdateView.as_view(),
        name="teacher_update",
    ),
    path(
        "teacher/delete/<int:pk>/",
        views.TeacherDeleteView.as_view(),
        name="teacher_delete",
    ),
    
    
    # For Subject Teacher (CRU) [DONE]
    path("subjectTeacher/", views.SubjectTeacherListView.as_view(), name="subjectTeacher"),
    path("subject_teacher/create",views.SubjectTeacherCreateView.as_view(),name="subject_teacher"),
    path("subject_teacher/update/<int:pk>/",views.SubjectTeacherUpdateView.as_view(),name="subject_teacher_update"),
    path(
        "subject_teacher/delete/<int:pk>/",
        views.SubjectTeacherDeleteView.as_view(),
        name="subject_teacher_delete",
    ),
    
    
    # For Enrollment (C) [DONE]
    path("enrollment/", views.EnrollmentListView.as_view(), name="enrollment"),
    path("enrollment/create", views.EnrollmentCreateView.as_view(), name="enrollment_post"),
    
    
    # For Result (C) [DONE] 
    path("results/", views.ResultListView.as_view(), name="results"),
    # path("results/create", views.ResultListView.as_view(), name="results_post"),
    
    
    # For Attendance (C) [DONE]
    path("attendance/", views.AttendanceListView.as_view(), name="attendance"),
    # path("attendance/create", views.AttendanceListView.as_view(), name="attendance_post"),
    
    
    # For Detail View Profile (C) [DONE]
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="profile"),
]
