from django.contrib import admin

# Register your models here.

from comment.models import Relpy,Comment

admin.site.register(Comment)
admin.site.register(Relpy)