from django import forms
from .models import *


# Create your forms here
# Create Student
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "email": forms.EmailInput(
                attrs={"type": "email", "class": "form-control email-field"}
            )
        }


# Create Teacher
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        widgets = {
            "email": forms.EmailInput(attrs={"type": "email"}),
        }


#  For Subject
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "credit_hours"]
        widgets = {
            "name": forms.TextInput(
                attrs={"type": "text", "class": "form-control name-field"}
            ),
            "credit_hours": forms.TextInput(
                attrs={
                    "type": "number",
                    "min": "0",
                    "class": "form-control credit-hours-field",
                }
            ),
        }


# For Exam Form
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["name", "subject", "exam_type", "date", "start_time", "end_time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
