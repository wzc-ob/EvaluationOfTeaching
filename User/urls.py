from django.urls import path

from User import views
app_name = 'User'
urlpatterns = [
    path('login/',views.Login.as_view(),name = 'login'),
    path('modify',views.Modify.as_view(),name = 'modify'),
    path('modifyajax/',views.modifyajax,name = 'modifyajax'),
    path('loginajax/',views.loginajax,name = 'loginajax'),
    path('logout/',views.logoutuser,name = 'logout')
]