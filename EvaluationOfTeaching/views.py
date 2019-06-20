import ast
import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Func, Count, Max, Min, Sum, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from EvaluationOfTeaching.forms import StudentForm, TeacherForm, SubjectForm, AddUserForm, ArticleForm
from User.models import Student, Teacher, S_Course, Course, T_Course, Evaluation, Subject, Administrators
import datetime

from article.models import Article
from comment.models import Relpy, Comment

"""主页"""


# 首页
def home(request):
    administrators = Administrators.objects.filter(user_id=request.user.id).exists()
    if administrators:
        request.session['user_type'] = 'administrators'
        return redirect(reverse('administratorshome'))
    else:
        teacher = Teacher.objects.filter(user_id=request.user.id).exists()
        if teacher:
            request.session['user_type'] = 'teacher'
            return redirect(reverse('teacherhome'))
        else:
            student = Student.objects.filter(user_id=request.user.id).exists()
            if student:
                request.session['user_type'] = 'student'
                return redirect(reverse("studenthome"))
            else:
                forms = Article.objects.all()
                return render(request, 'home.html', {'blogs': forms})


class Articleview(View):
    def get(self, request, article_id):
        article = Article.objects.filter(id=article_id).first()
        dicts = {}
        comments = Comment.objects.filter(article_id=article_id).all()
        for comment in comments:
            replys = Relpy.objects.filter(reply_id=comment.id).all()
            dicts[comment] = replys
        # return HttpResponse(dicts)
        return render(request, 'blog.html', {'article': article, 'dicts': dicts})

    @method_decorator(login_required)
    def post(self, request, article_id):
        if request.user.id:
            article_id = request.POST['article_id']
            user_id = request.user.id
            comment = request.POST['comment']
            com = Comment(article_id=article_id, user_id=user_id, comment=comment)
            com.save()
            return self.get(request, article_id)
        else:
            return redirect(reverse('user:login'))


"""学生功能模块 """


# 学生首页新闻界面
@login_required
def studentHome(request):
    forms = Article.objects.all()
    return render(request, 'student/studenthome.html', {'blogs': forms})


# 新闻界面
class StudentArticleview(View):
    def get(self, request, article_id):
        texts = {'name': 'name'}
        article = Article.objects.filter(id=article_id).first()
        dicts = {}
        comments = Comment.objects.filter(article_id=article_id).all()
        for comment in comments:
            replys = Relpy.objects.filter(reply_id=comment.id).all()
            dicts[comment] = replys
        return render(request, 'student/studentblog.html', {'article': article, 'dicts': dicts})

    @method_decorator(login_required)
    def post(self, request, article_id):
        if request.user.id:
            article_id = request.POST['article_id']
            user_id = request.user.id
            comment = request.POST['comment']
            com = Comment(article_id=article_id, user_id=user_id, comment=comment)
            com.save()
            return self.get(request, article_id)
        else:
            return redirect(reverse('user:login'))


# 回复界面
@login_required
def reply(request, article_id):
    if request.method == 'POST':
        reply_id_id = request.POST.get('reply_id_id')
        user_id = request.user.id
        reply = request.POST.get('reply')
        rep = Relpy(reply=reply, user_id=user_id, reply_id_id=reply_id_id)
        rep.save()
        url = '/student/article/' + article_id
        return redirect(url)


# 查看个人信息
class StudentInformation(View):
    def get(self, request):
        student = Student.objects.get(user_id=request.user.id)
        form = StudentForm(instance=student)
        return render(request, 'student/studentinformation.html', {'form': form})

    def post(self, request):
        student = Student.objects.get(user_id=request.user.id)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
        else:
            error = form.errors
            return render(request, 'student/studentinformation.html', {'form': form, 'error': error})

        return redirect(reverse('studentinformation'))


# 未评价的教师
def notEvaluated(request):
    student = Student.objects.get(user_id=request.user.id)
    teachers = Teacher.objects.filter(t_course__s_course__student_id=student.id).exclude(
        evaluation__student=student.id).distinct()
    return render(request, 'student/notevaluate.html', {'teachers': teachers})


# 已经评价的教师
def alreadyEvaluated(request):
    student = Student.objects.get(user_id=request.user.id)
    teachers = Teacher.objects.filter(evaluation__student=student.id)
    return render(request, 'student/alreadyevaluate.html', {'teachers': teachers})


# 已选的课程
def selectedCourses(request):
    s_courses = S_Course.objects.filter(student__user_id=request.user.id)
    return render(request, 'student/selected.html', {'s_courses': s_courses})


# 待选的课程
def unselectedCourses(request):
    student = Student.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        search = request.POST.get('search')
        coursers = Course.objects.filter(
            Q(cname__contains=search) | Q(t_course__teacher__name__contains=search)).exclude(
            t_course__s_course__student_id=student.id).distinct()
        return render(request, 'student/unselected.html', {'courses': coursers})
    else:

        coursers = Course.objects.exclude(t_course__s_course__student_id=student.id)
        return render(request, 'student/unselected.html', {'courses': coursers})


# 选课(跳转到详细界面)
def choice(request, course_id):
    t_courses = T_Course.objects.filter(course_id=course_id)
    return render(request, 'student/selecteteacher.html', {'t_courses': t_courses})


# 添加课程(选择具体老师)
def add(request, course_id, teacher_id):
    t_course = T_Course.objects.get(course_id=course_id, teacher_id=teacher_id)
    student = Student.objects.get(user_id=request.user.id)
    s_course = S_Course(student_id=student.id, t_course_id=t_course.id)
    s_course.save()
    return redirect(reverse('unselected'))


# 删除课程
def delete(request, course_id, teacher_id):
    t_course = T_Course.objects.get(course_id=course_id, teacher_id=teacher_id)
    student = Student.objects.get(user_id=request.user.id)
    s_course = S_Course.objects.get(student_id=student.id, t_course_id=t_course.id)
    s_course.delete()
    return redirect(reverse('selectedcourses'))


# 评价老师
def evaluated(request, teacher_id):
    subjects = Subject.objects.all()
    if request.method == 'GET':
        return render(request, 'student/subject.html', {'subjects': subjects})
    if request.method == 'POST':
        opinion = request.POST.get('opinion')
        result = {}
        number = 0
        student = Student.objects.get(user_id=request.user.id)
        for subject in subjects:
            number += int(request.POST[str(subject.subject)])
            result[str(subject.subject)] = request.POST[str(subject.subject)]
        evaluation = Evaluation(student_id=student.id, teacher_id=teacher_id, result=str(result), score=number,opinion=opinion)
        evaluation.save()
        return redirect(reverse('notevaluated'))


# 查看优秀老师
def studentsee(request):
    teachers = Evaluation.objects.values('teacher').annotate(avg=Round(Avg('score'))).values('teacher__name',
                                                                                             'avg').order_by('-avg')[
               0:5]
    return render(request, 'student/prominentteacher.html', {"teachers": teachers})


"""老师功能模块 """


# 教师首页
@login_required
def teacherHome(request):
    return render(request, 'teacher/teacherhome.html')

#查看学生意见
def seeOpinion(request):
    evaluation = Evaluation.objects.filter(teacher__user_id =request.user.id).values('opinion')
    return render(request,'teacher/seeOpinion.html',{'evaluation':evaluation})



# 查看个人信息
class TeacherInformation(View):
    def get(self, request):
        teacher = Teacher.objects.get(user_id=request.user.id)
        form = TeacherForm(instance=teacher)
        return render(request, 'teacher/teacherinformation.html', {'form': form})

    def post(self, request):
        teacher = Teacher.objects.get(user_id=request.user.id)
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
        else:
            error = form.errors
            return render(request, 'teacher/teacherinformation.html', {'form': form, 'error': error})
        return redirect(reverse('teacherinformation'))


# 查看优秀老师
def teachersee(request):
    teachers = Evaluation.objects.values('teacher').annotate(avg=Round(Avg('score'))).values('teacher__name',
                                                                                             'avg').order_by('-avg')[
               0:5]
    return render(request, 'teacher/teachersee.html', {"teachers": teachers})


# 查看教授课程
def teachcourse(request):
    courses = S_Course.objects.values('t_course').annotate(sum=Count('student')).filter(
        t_course__teacher__user_id=request.user.id).values('t_course__course_id', 't_course__course__cname', 'sum')
    return render(request, 'teacher/teachcourse.html', {'courses': courses})


# 查看选课学生
def checkStudent(request, course_id):
    students = S_Course.objects.filter(t_course__teacher__user_id=request.user.id).filter(
        t_course__course_id=course_id).order_by('id')
    # students = Student.objects.filter(s_course__t_course__teacher__user_id = request.user.id).order_by('id')
    return render(request, 'teacher/checkStudent.html', {'students': students})


# 查看评教状态
def checkEvaluated(request):
    students = Student.objects.filter(evaluation__teacher__user_id=request.user.id).order_by('id')
    return render(request, 'teacher/checkEvaluated.html', {'students': students})


# 查看评价明细
def evaluateDetail(request):
    evaluations = Evaluation.objects.filter(teacher__user_id=request.user.id).order_by('-score')
    return render(request, 'teacher/evaluateDetail.html', {'evaluations': evaluations})


# 查看单个评价
def seeSingleEvaluated(request, evaluation_id):
    evaluate = Evaluation.objects.get(id=evaluation_id)
    result = evaluate.result
    result = ast.literal_eval(result)
    return render(request, 'teacher/seeSingleEvaluated.html', {'result': result})


# 评价统计
def personalscores(request):
    teacher = Evaluation.objects.filter(teacher__user_id=request.user.id).aggregate(Count('student'), Avg('score'),
                                                                                    Max('score'), Min('score'),
                                                                                    Sum('score'))

    return render(request, 'teacher/personalscores.html', {'teacher': teacher})


# 查看单项分数
def singleScore(request):
    subjects = Subject.objects.all().values_list('subject', flat=True)
    evaluations = Evaluation.objects.filter(teacher__user_id=request.user.id).order_by('-score')
    count = Evaluation.objects.filter(teacher__user_id=request.user.id).aggregate(Count('result'))
    count = count['result__count']
    context = {}
    for i, value in enumerate(list(subjects)):
        context[value] = 0
        for evaluation in evaluations:
            result = ast.literal_eval(evaluation.result)
            values = list(result.values())
            context[value] += int(values[i])
        if count != 0:
            context[value] = context[value] / count
    return render(request, 'teacher/singleScore.html', {'context': context})


# 查看优秀老师
# 设置小数点
class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


def see(request):
    teachers = Evaluation.objects.values('teacher').annotate(avg=Round(Avg('score'))).values('teacher__name',
                                                                                             'avg').order_by('-avg')[
               0:5]
    return render(request, 'prominentteacher.html', {"teachers": teachers})


"""管理员模块"""


#  首页
def administrators(request):
    return render(request, 'administrators/administratorshome.html')


# 编辑新闻
def article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('article'))
        else:
            error = form.errors
            return render(request, 'administrators/article.html', {'form': form,'error':error})
    else:
        form = ArticleForm()
        return render(request, 'administrators/article.html', {'form': form})


# 查看所有老师分数
def seescore(request):
    teachers = Evaluation.objects.values('teacher').annotate(avg=Round(Avg('score'))).values('teacher__name',
                                                                                             'avg').order_by('-avg')
    return render(request, 'administrators/seeteacherscore.html', {"teachers": teachers})


# 查看该老师单项得分
def singleTeacherScore(request, teacher_id):
    subjects = Subject.objects.all().values_list('subject', flat=True)
    evaluations = Evaluation.objects.filter(teacher_id=teacher_id).order_by('-score')
    count = Evaluation.objects.filter(teacher_id=teacher_id).aggregate(Count('result'))
    count = count['result__count']
    context = {}
    for i, value in enumerate(list(subjects)):
        context[value] = 0
        for evaluation in evaluations:
            result = ast.literal_eval(evaluation.result)
            values = list(result.values())
            context[value] += int(values[i])
        if count != 0:
            context[value] = context[value] / count
    return render(request, 'administrators/singleScore.html', {'context': context})


# 查看评价题目
def seeSubject(request):
    subjects = Subject.objects.all()
    return render(request, 'administrators/seeSubject.html', {'subjects': subjects})


# 修改题目
def modifySubject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            if request.POST.get('subject') == subject.subject:
                return JsonResponse('您没有做出任何更改', safe=False)
            form.save()
            return JsonResponse('success', safe=False)
        else:
            return JsonResponse('题目过长', safe=False)
    else:
        form = SubjectForm(instance=subject)
        return render(request, 'administrators/modifySubject.html', {'form': form})


# 增加题目
def addSubject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = Subject.objects.filter(subject=request.POST.get('subject')).exists()
            if subject:
                data = '改题目已经存在'
            else:
                form.save()
                data = 'success'
        else:
            if request.POST.get('subject') == '':
                data = '题目为空'
            else:
                data = '题目过长'
        return JsonResponse(data, safe=False)
    else:
        form = SubjectForm()
        return render(request, 'administrators/addSubject.html', {'form': form})


# 删除题目
def deleteSubject(request, subject_id):
    subjects = Subject.objects.get(id=subject_id)
    subjects.delete()
    return redirect(reverse('seeSubject'))


# 增加学生用户
def addStudent(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            password = request.POST.get('password')
            name = request.POST.get('name')
            user = User.objects.create_user(username=user_id, password=password)
            # user.save()
            student = Student(user_id=user.id, name=name)
            student.save()
            return redirect(reverse('addStudent'))
        else:
            error = form.errors
            return render(request, 'administrators/addStudent.html', {'form': form, 'error': error})
    else:
        form = AddUserForm()
        return render(request, 'administrators/addStudent.html', {'form': form})


# 增加老师用户
def addTeacher(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            password = request.POST.get('password')
            name = request.POST.get('name')
            user = User.objects.create_user(username=user_id, password=password)
            student = Teacher(user_id=user.id, name=name)
            student.save()
            return redirect(reverse('addTeacher'))
        else:
            error = form.errors
            return render(request, 'administrators/addTeacher.html', {'form': form, 'error': error})
    else:
        form = AddUserForm()
        return render(request, 'administrators/addTeacher.html', {'form': form})
