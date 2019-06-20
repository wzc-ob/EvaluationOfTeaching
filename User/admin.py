from django.contrib import admin


# Register your models here.
from .models import Student,Teacher,Course,T_Course,S_Course,Subject,Evaluation,Administrators

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(T_Course)
admin.site.register(S_Course)
admin.site.register(Subject)
admin.site.register(Evaluation)
admin.site.register(Administrators)
