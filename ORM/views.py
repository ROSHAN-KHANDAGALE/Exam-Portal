from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

# For Model
from django.contrib.auth.models import User
from .models import *
from .forms import *

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

        return render(request, "user/home.html")


# For Student Registeration
class StudentRegister(View):
    def get(self, request):
        form = StudentForm()
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


# Random Subject Code Generator
subj_code = random.randint(0, 9999)


# For Teacher
class TeacherListView(ListView):
    pass


# For Subject
class SubjectListView(ListView):
    model = Subject
    form_class = SubjectForm
    template_name = "admin/subject.html"
    paginate_by = 5
    context_object_name = "subjects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


# For Subject Post/ Create View
class SubjectCreateView(CreateView):
    model = Subject
    initial = {"code": subj_code}
    fields = ["name", "credit_hours"]
    template_name = "admin/subject.html"
    success_url = "/subject/"


# For Exam
class ExamListView(ListView):
    model = Exam
    form_class = ExamForm
    template_name = "admin/examForm.html"
    paginate_by = 5
    context_object_name = "exams"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class ExamCreateView(CreateView):
    model = Exam
    fields = "__all__"
    template_name = "admin/examForm.html"
    success_url = "/examForm/"
