"""EvaluationOfTeaching URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from EvaluationOfTeaching import views
from django.conf import settings

urlpatterns = [
                  # 首页
                  path('', views.home, name='home'),
                  path('see/', views.see, name='see'),
                  path('/<article_id>', views.Articleview.as_view(), name='article'),
                  # 后台
                  path('admin/', admin.site.urls),
                  # 学生
                  path('student/', views.studentHome, name='studenthome'),
                  path('student/not/', views.notEvaluated, name='notevaluated'),
                  path('student/already/', views.alreadyEvaluated, name='alreadyevaluated'),
                  path('student/selected/', views.selectedCourses, name='selectedcourses'),
                  path('student/unselected/', views.unselectedCourses, name='unselected'),
                  path('student/choice/<course_id>', views.choice, name='choice'),
                  path('student/choice/<course_id>/<teacher_id>', views.add, name='add'),
                  path('student/delete/<course_id>/<teacher_id>', views.delete, name='delete'),
                  path('student/evaluated/<teacher_id>', views.evaluated, name='evaluated'),
                  path('student/studentinformation/', views.StudentInformation.as_view(), name='studentinformation'),
                  path('student/studentsee/', views.studentsee, name='studentsee'),
                  path('student/article/<article_id>', views.StudentArticleview.as_view(), name='student_article'),
                  path('student/article/rep ly/<article_id>', views.reply, name='reply'),
                  # 教师
                  path('teacher/', views.teacherHome, name='teacherhome'),
                  path('teacher/checkStudent/<course_id>', views.checkStudent, name='checkStudent'),
                  path('teacher/checkEvaluated/', views.checkEvaluated, name='checkEvaluated'),
                  path('teacher/teacherinformation/', views.TeacherInformation.as_view(), name='teacherinformation'),
                  path('teacher/teachersee/', views.teachersee, name='teachersee'),
                  path('teacher/personalscores/', views.personalscores, name='personalscores'),
                  path('teacher/teachcourse/', views.teachcourse, name='teachcourse'),
                  path('teacher/seeSingleEvaluated/<evaluation_id>', views.seeSingleEvaluated,
                       name='seeSingleEvaluated'),
                  path('teacher/evaluateDetail', views.evaluateDetail, name='evaluateDetail'),
                  path('teacher/singleScore', views.singleScore, name='singleScore'),
                  path('teacher/seeOpinion', views.seeOpinion, name='seeOpinion'),

                  # 管理员
                  path('administrators/', views.administrators, name='administratorshome'),
                  path('administrators/seescore/', views.seescore, name='seescore'),
                  path('administrators/seeSubject/', views.seeSubject, name='seeSubject'),
                  path('administrators/modifySubject/<subject_id>', views.modifySubject, name='modifySubject'),
                  path('administrators/addSubject/', views.addSubject, name='addSubject'),
                  path('administrators/deleteSubject/<subject_id>', views.deleteSubject, name='deleteSubject'),
                  path('administrators/addStudent/', views.addStudent, name='addStudent'),
                  path('administrators/addTeacher/', views.addTeacher, name='addTeacher'),
                  path('administrators/singleTeacherScore/<teacher_id>/', views.singleTeacherScore,
                       name='singleTeacherScore'),
                  path('administrators/article/', views.article, name='article'),
                  # 用户
                  path('user/', include('User.urls', namespace='user')),
                  # 扩展
                  path('ckeditor/', include('ckeditor_uploader.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
