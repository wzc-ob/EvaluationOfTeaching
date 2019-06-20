# 此仅当示例逻辑代码，代码逻辑情况根据个人而定
# 博主的代码中用户类型为登录时添加到session存储
# 博主项目中的不同用户的访问路由前均以用户名开头，以方便辨认以及以下代码逻辑的可用性


from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class Filter(MiddlewareMixin):
    def process_request(self, request):
        # 获取路由的首个字段
        request_type = (request.path).split("/")[1]
        if request_type == '' or request_type == 'user' or request_type =='media' or request_type == 'see' or request_type == 'admin' or request_type == 'ckeditor':
            pass
        else:
            if request.user.id is None:
                return HttpResponse(status=404)
            else:
                # 获取用户的类型
                user_type = request.session.get('user_type')
                if user_type == request_type:
                    pass
                else:
                    return HttpResponse(status=404)
                # if user_type == "student":
                #     if request_type == "student":
                #         pass  # 如何用户类型与路由匹配，直接通过
                #     else:
                #         return HttpResponse(status=404)  # 用户类型不匹配返回状态码404
                # elif user_type == "teacher":
                #     if request_type == "teacher":
                #         pass  # 如何用户类型与路由匹配，直接通过
                #     else:
                #         return HttpResponse(status=404)  # 用户类型不匹配返回状态码404


