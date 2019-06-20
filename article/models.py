from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils import timezone


class Article(models.Model):
    abstract = models.CharField(max_length=100)
    title = models.CharField(max_length=20)
    img = models.ImageField(upload_to='files', blank=True,default= 'nopic.jpg')
    date = models.DateField()
    article = RichTextUploadingField(verbose_name='内容')
    class Meta:
        db_table = 'e_artcle'
