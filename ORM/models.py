from django.db import models
from django.contrib.auth.models import User
import random


# Create your models here.
class ResetID(models.Model):
    UUID = models.UUIDField(unique=True)
    reset_entry = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.UUID} {self.reset_entry} {self.user} {self.expiry} {self.is_expired} "


# Student registration
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=15)
    enrollment_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.enrollment_no})"


# Random Subject Code generator
def generate_code():
    return f"{random.randint(0, 9999):04}"


# Subjects
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4, unique=True, default=generate_code)
    credit_hours = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


# Teacher registration
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Prof. {self.first_name} {self.last_name}"


# Exams
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ("MCQ", "Multiple Choice Questions"),
        ("Theory", "Theory Exam"),
        ("Practical", "Practical Exam"),
    ]

    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.exam_type})"


# Student exam results
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    def __str__(self):
        return f"{self.student.first_name} - {self.exam.name} ({self.marks_obtained}/{self.total_marks})"


# Assigning teachers to subjects
class SubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} by Prof. {self.teacher.first_name} {self.teacher.last_name}"


# Student enrollment in subjects
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} enrolled in {self.subject.name}"


# Attendance
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()

    def __str__(self):
        return f"{self.student.first_name} - {self.subject.name} on {self.date} ({'Present' if self.status else 'Absent'})"
