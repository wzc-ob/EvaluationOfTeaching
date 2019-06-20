import re
from django import forms
from django.forms import TextInput

from User.models import Student, Teacher, Subject
from  django.contrib.admin import widgets

from article.models import Article


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['team','name','sex','birthday','img','telephone']
    def clean_sex(self):
        sex = self.cleaned_data.get('sex')
        if sex == '男' or sex == '女':
            return sex
        else:
            raise forms.ValidationError('性别错误，请输入男或女')
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        mobile_regex = r'^1[34578]\d{9}$'
        p = re.compile(mobile_regex)
        if p.match(telephone):
            return telephone
        else:
            raise forms.ValidationError('手机号码非法', code='invalid mobile')
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['user']

    def clean_sex(self):
            sex = self.cleaned_data.get('sex')
            if sex == '男' or sex == '女':
                return sex
            else:
                raise forms.ValidationError('性别错误，请输入男或女')
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        mobile_regex = r'^1[34578]\d{9}$'
        p = re.compile(mobile_regex)
        print(p.match(telephone))
        if p.match(telephone):
            return telephone
        else:
            raise forms.ValidationError('手机号码非法', code='invalid mobile')
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['id','subject']
class AddUserForm(forms.Form):
    user_id = forms.CharField(max_length=9,min_length=5,widget=forms.TextInput({'placeholder':'账号'}))
    password = forms.CharField(label=('Password'),max_length=12,min_length=8,widget=forms.PasswordInput({'placeholder':'密码'}))
    name = forms.CharField(max_length=4,min_length=2,widget=forms.TextInput({'placeholder':'姓名'}))
    def clean_name(self):
        name = self.cleaned_data.get('name')
        name_regex = '^([\u4e00-\u9fa5]){2,4}$'
        p = re.compile(name_regex)
        if p.match(name):
            return name
        else:
            raise forms.ValidationError('输入正确的姓名', code='invalid name')
    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        user_id_regex = '^[1,2][0-9]{4,8}$'
        p = re.compile(user_id_regex)
        print(p.match(user_id))
        if p.match(user_id):
            return user_id
        else:
            raise forms.ValidationError('请输入正确的账号', code='invalid name')
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'date' : TextInput({'type':'data','required':'required'})
        }

