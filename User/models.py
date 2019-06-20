from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

class Administrators(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=4,default='王同学')
    team = models.CharField(max_length=8,default='软件151')
    sex = models.CharField(max_length=1,default='男')
    birthday = models.DateField(default='1996-02-02')
    img = models.ImageField(upload_to='files',default='nopic.jpg',blank = True)
    telephone = models.CharField(max_length=11,default='18772815717')
    class Meta:
        db_table = 'e_student'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=12, default='王老师')
    sex = models.CharField(max_length=3, default='男')
    birthday = models.DateField(default='1996-02-02')
    img = models.ImageField(upload_to='files', default='nopic.jpg', blank=True)
    telephone = models.CharField(max_length=11, default='18772815717')
    age = models.CharField(max_length=3,default = 30)
    class Meta:
        db_table = 'e_teacher'

class Course(models.Model):
    cname = models.CharField(max_length=100)
    class Meta:
        db_table = 'e_course'

class T_Course(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    class Meta:
        db_table = 'e_t_couser'

class S_Course(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    t_course = models.ForeignKey(T_Course,on_delete=models.CASCADE)
    class Meta:
        db_table = 'e_s_couser'

class Subject(models.Model):
    subject = models.CharField(max_length=200)
    class Meta:
        db_table = 'e_subject'

class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    result = models.CharField(max_length= 300)
    score = models.IntegerField(default=18)
    opinion = models.CharField(max_length=200,default='好')
    class Meta:
        db_table = 'e_evaluation'
