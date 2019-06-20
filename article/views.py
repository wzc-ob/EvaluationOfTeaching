# from audioop import reverse
#
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect ,HttpResponse
# from django.utils.decorators import method_decorator
# from django.views import View
# from django.views.generic import ListView
#
# from article.models import Article
# from comment.models import Relpy, Comment
#
#
# class Articleview(View):
#     def get(self, request,article_id):
#         texts = {'name':'name'}
#         article = Article.objects.filter(id=article_id).first()
#         dicts = {}
#         comments = Comment.objects.filter(article_id=article_id).all()
#         for comment in comments:
#             replys = Relpy.objects.filter(reply_id=comment.id).all()
#             dicts[comment] = replys
#         print(type(article))
#         print(dicts)
#         # return HttpResponse(dicts)
#         return render(request,'blog.html',{'article':article,'dicts':dicts})
#
#     @method_decorator(login_required)
#     def post(self,request,article_id):
#         if request.user.id:
#             article_id = request.POST['article_id']
#             user_id = request.user.id
#             comment = request.POST['comment']
#             com = Comment(article_id=article_id,user_id=user_id,comment=comment)
#             com.save()
#
#             return  self.get(request,article_id)
#         else:
#             return redirect(reverse('user:login'))
#
# @login_required
# def comment(request,article_id,reply_id_id):
#     article_id = article_id
#     reply_id_id = request.POST['id']
#     user_id = request.user.id
#     reply = request.POST['reply']
#     # print(user_id,reply_id_id,reply)
#     rep = Relpy(reply = reply,user_id = user_id, reply_id_id = reply_id_id)
#     rep.save()
#     return Articleview().get(request,article_id)
#
# def imglist(request):
#     forms = Article.objects.all()
#     return render(request,'bloglist.html',{'blogs':forms})
#
# class ArticleListView(ListView):
#     model = Article
#     template_name = 'bloglist.html'
#     paginate_by = 100
#     context_object_name = 'blogs'
#     ordering = 'data'
#     page_kwarg = 'page'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ArticleListView, self).get_context_data(**kwargs)
#         return context
#
#     def get_queryset(self):
#         return Article.objects.all().order_by('date')