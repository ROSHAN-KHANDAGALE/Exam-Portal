from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.ResetID)
admin.site.register(models.Student)
admin.site.register(models.Subject)
admin.site.register(models.Teacher)
admin.site.register(models.Exam)
admin.site.register(models.Result)
admin.site.register(models.SubjectTeacher)
admin.site.register(models.Enrollment)
admin.site.register(models.Attendance)
