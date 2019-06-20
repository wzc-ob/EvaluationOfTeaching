from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Comment(models.Model):
    article = models.ForeignKey('article.Article',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    class Meta:
        db_table = 'e_comment'

class Relpy(models.Model):
    reply_id = models.ForeignKey(Comment,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user' ,on_delete=models.CASCADE)
    reply = models.CharField(max_length=100)
    class Meta:
        db_table = 'e_relpy'
