from django import forms
from .models import *


# Create your forms here
# Create Student
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "phone_no"]
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


# For Subject Teacher
class SubjectTeacherForm(forms.ModelForm):
    class Meta:
        model = SubjectTeacher
        fields = "__all__"


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


# For Enrollment Form
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"


# For Results Form
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = "__all__"


# For Attendance Form
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"


# For Profile
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "profile_photo",
            "contact_number",
        ]

        widgets = {
            "profile_photo": forms.FileInput(
                attrs={"type": "file", "accept": "image/*"}
            ),
        }

        def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)

            # Add custom CSS classes to form fields
            self.fields["username"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Username"}
            )
            self.fields["first_name"].widget.attrs.update(
                {"class": "form-control", "placeholder": "First Name"}
            )
            self.fields["last_name"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Last Name"}
            )
            self.fields["email"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Email"}
            )
            self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})
            self.fields["profile_photo"].widget.attrs.update(
                {"class": "form-control-file", "type": "file", "accept": "image/*"}
            )
            self.fields["contact_number"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Contact Number"}
            )
