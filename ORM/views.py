from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy

# For Model
from .models import *
from .forms import *

# For searching and pagination
from django.db.models import Q
from django.core.paginator import Paginator

# For Authentication, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# For authenticated Access
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# For sending Mail
from django.core.mail import send_mail

# For UUID, Date & Time
import uuid, datetime, random
from pytz import timezone


# Create your views here.
# For Index
class Login(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        email = request.POST.get("email_or_username")
        password = request.POST.get("pass")
        try:
            user_Email = User.objects.get(email=email)
            username = user_Email.username
        except User.DoesNotExist:
            username = email
            messages.error(request, "User Doesn't Exist")
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect("home/")
        else:
            messages.error(request, "Invalid Credentials!!")
            return redirect("/")


# For Registering
class Signup(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("pass")
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return render(request, "signup.html")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email ID Exists!!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username Exists")
        else:
            user = User.objects.create_user(
                first_name=firstName,
                last_name=lastName,
                email=email,
                username=username,
                password=password,
            )
            user.save()
            return redirect("/")
        return render(request, "signup.html")


# For Forgot
class Forgot(View):
    def get(self, request):
        return render(request, "forgot.html")

    def post(self, request):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            reset_id = uuid.uuid1(random.randint(0, 281474976710655))
            current_datetime = datetime.datetime.now()
            user = User.objects.get(email=email)
            expiry_date = current_datetime + datetime.timedelta(minutes=5)
            if current_datetime < expiry_date:
                is_expiry = False
            else:
                is_expiry = True
            forgot = ResetID(
                UUID=reset_id,
                reset_entry=current_datetime,
                user=user,
                expiry=expiry_date,
                is_expired=is_expiry,
            )
            forgot.save()
            URL = f"{settings.SITE_URL}/{reset_id}"
            if email:
                subject = "Reset Password Request - Exam Portal"
                message = f"""
Dear {user.username},
We received a request to reset your account password for the Exam Portal. To proceed with resetting your password, please click the link below:
Reset Password: {URL}
If you did not request this password reset, kindly ignore this message, and your password will remain unchanged.
Please note that for security purposes, this link will expire in 5 minutes.
Best Regards,  
Exam Portal Team  
---
This is an automated email. Please do not reply to this message. If you have any questions, contact our support team at roshan@examportal.com.
"""
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                    messages.success(request, "Email Sended Successfully")
                    return redirect("/")
                except Exception:
                    return render(request, "forgot.html")
            else:
                return render(request, "forgot.html")
        else:
            messages.error(request, f"Email Address {email}, Does not exists!")
        return render(request, "forgot.html")


# For Reset
class Reset(View):
    def get(self, request, uuid):
        return render(request, "reset.html", {"uuid": uuid})

    def post(self, request, uuid):
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        current_timedate = datetime.datetime.now()
        reset_uuid = ResetID.objects.get(UUID=uuid)
        user = reset_uuid.user
        current_time = current_timedate.astimezone(timezone("UTC"))
        if current_time < reset_uuid.expiry and new_password == confirm_password:
            user.set_password(confirm_password)
            user.save()
            return redirect("/")
        else:
            return redirect("/")


# For Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


# For Home
class Home(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_superuser:
            return render(request, "admin/admin_dashboard.html")
        else:
            return render(request, "user/home.html")


# For Settings
class Settings(View):
    def get(self, request):
        return render(request, "admin/settings.html")


# For Student Registeration (CRUD) (DONE)
# For Read Student
class StudentRegister(View):
    def get(self, request):
        form = StudentForm()
        query = request.GET.get("q")

        if query:
            registered_data = Student.objects.filter(name__icontains=query)
        else:
            registered_data = Student.objects.all()

        return render(
            request,
            "admin/studentRegister.html",
            {"form": form, "registered_data": registered_data},
        )

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Registered!!!")
            return redirect("studentRegister")
        else:
            messages.error(request, "Registration Failed!!")
            return redirect("studentRegister")


# For Updating Student
class StudentUpdate(View):
    def get(self, request, id):
        fetch = Student.objects.get(id=id)
        form = StudentForm(instance=fetch)
        registered_data = Student.objects.all()
        return render(
            request,
            "admin/studentRegister.html",
            {"fetch": fetch, "form": form, "registered_data": registered_data},
        )

    def post(self, request, id):
        fetch = Student.objects.get(id=id)
        form = StudentForm(request.POST, instance=fetch)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Updated Successfully!")
            registered_data = Student.objects.all()
            return render(
                request,
                "admin/studentRegister.html",
                {"form": form, "registered_data": registered_data},
            )
        else:  #
            messages.error(request, "Failed to Update the Student!")
            return redirect("studentRegister")


# For Delete Student
class StudentDelete(View):
    def get(self, request, id):
        Student.objects.get(id=id).delete()
        messages.success(self.request, "Student removed Successfully!!")
        return redirect("studentRegister")


# For Teacher (CRU)
# For View/ Read
class TeacherListView(ListView):
    model = Teacher
    form_class = TeacherForm
    template_name = "admin/teacher.html"
    context_object_name = "teachers"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q", "")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(email__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        context["search_query"] = self.request.GET.get("q", "")
        return context


# For Teacher Post/Create View
class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "admin/teacher.html"

    # Custom Redirect
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Teacher Registered Successfully")
        return redirect("teacher")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something Went Wrong!!")
        return response


# Udate Teacher
class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "admin/teacher.html"

    def form_valid(self, form):
        self.object = form.save()
        messages.error(self.request, "Successfully updated Record!!")
        return redirect("teacher")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something Went Wrong!!")
        return response


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = "admin/teacher.html"
    success_url = reverse_lazy("/teacher/")


# For Subject (CR)
# For Subject View
class SubjectListView(ListView):
    model = Subject
    form_class = SubjectForm
    template_name = "admin/subject.html"
    context_object_name = "subjects"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q", "")

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        context["search_query"] = self.request.GET.get("q", "")
        return context


# For Subject Post/ Create View
class SubjectCreateView(CreateView):
    model = Subject
    fields = ["name", "credit_hours"]
    template_name = "admin/subject.html"
    success_url = "/subject/"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Subject created successfully!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something went wrong!")
        return response


# For Exam (CR)
# For Exam View
class ExamListView(ListView):
    model = Exam
    form_class = ExamForm
    template_name = "admin/examForm.html"
    context_object_name = "exams"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


# For Exam Create
class ExamCreateView(CreateView):
    model = Exam
    fields = "__all__"
    template_name = "admin/examForm.html"
    success_url = "/examForm/"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        messages.success(self.request, "Exam Created successfully!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something went wrong!")
        return response


# For Subject Teacher (CRU) [DONE]
# For Subject Teacher View
class SubjectTeacherListView(ListView):
    model = SubjectTeacher
    form_class = SubjectTeacherForm
    template_name = "admin/SubjectTeacher.html"
    context_object_name = "subjectTeacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context


# For Subject Teacher Create
class SubjectTeacherCreateView(CreateView):
    model = SubjectTeacher
    form_class = SubjectTeacherForm
    success_url = "/subjectTeacher/"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        messages.success(self.request, "Incharge Allocated successfully!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something went wrong!")
        return response


# For Subject Teacher Update
class SubjectTeacherUpdateView(UpdateView):
    model = SubjectTeacher
    form_class = SubjectTeacherForm
    template_name = "admin/SubjectTeacher.html"

    def form_valid(self, form):
        self.object = form.save()
        messages.error(self.request, "Successfully updated Record!!")
        return redirect("subjectTeacher")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something Went Wrong!!")
        return response


class SubjectTeacherDeleteView(DeleteView):
    pass


# For Enrollment (CR)
# For Enrollment View
class EnrollmentListView(ListView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "admin/enrollment.html"
    context_object_name = "enrollment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context


class EnrollmentCreateView(CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    success_url = "/enrollment/"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        messages.success(self.request, "Incharge Allocated successfully!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something went wrong!")
        return response


# For Attendance (CR)
# For Attendance View
class AttendanceListView(ListView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "admin/attendance.html"
    context_object_name = "attendance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context


# For Result (CR)
# For Result View
class ResultListView(ListView):
    model = Result
    form_class = ResultForm
    template_name = "admin/results.html"
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        return context


# For Profile (CRU) [DONE]
# For Profile View
# Note: Detail view is used to fetch the specific user details
class ProfileDetailView(DetailView):
    model = User
    form_class = UserForm
    template_name = "admin/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["profile"]
        context["form"] = self.form_class(instance=user)
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successful!")
            return redirect("profile", pk=user.pk)
        else:
            messages.error(request, "Something went wrong!")
            return render(self.get_context_data(form=form))


# For User Side
# For Exam Side
class ExamShowcaseListView(ListView):
    model = Exam
    template_name = "user/exams.html"
    context_object_name = "examUser"
