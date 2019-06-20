import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from User.models import Student, Teacher, Course


# 登陆
class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    # def post(self, request):
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #             return redirect(reverse("home"))
    #     else:
    #         return render(request, 'login.html')


# 修改密码
class Modify(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'modify.html')
    # def post(self, request):
    #     password = request.POST['password']
    #     user = User.objects.get(id = request.user.id)
    #     print(password)
    #     if password :
    #         user.set_password(password)
    #         user.save()
    #         return redirect(reverse("user:login"))
    #     else:
    #         return render(request, 'modify.html')


# 注销登陆
def logoutuser(request):
    logout(request)
    return redirect(reverse('user:login'))

def modifyajax(request):
    password = request.POST.get('password')
    confirmpassword = request.POST.get('confirmpassworm')
    if password =='':
        data = '请输入密码'
    else:
        if confirmpassword =='':
            data = '请再次输入密码'
        else:
            if password == confirmpassword:
                user = User.objects.get(id=request.user.id)
                if user.check_password(password):
                    data = '您的密码没有进行更改'
                else:
                    user.set_password(password)
                    user.save()
                    data = 'success'
            else:
                data = '您输入的两次密码不一样'
    return JsonResponse(data, safe=False)

def loginajax(request):
    # username = request.POST.getlist('username')
    # print(json.loads(username[0])['name'])
    # user = json.loads(username)
    # print(user['name'])
    # print(dict(username[0]))
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username == '':
        data = '用户名为空'
    else:
        if password == '':
            data = '密码为空'
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # courses = Course.objects.filter(t_course__teacher__user_id=request.user.id).values('id','cname')
                    # courses = list(courses)
                    # return JsonResponse(courses, safe=False)
                    data = 'success'
            else:
                data = '你输入的账号或者密码错误'
                # return render(request, 'login.html')
    return JsonResponse(data, safe=False)
