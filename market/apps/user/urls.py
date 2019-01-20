from django.conf.urls import url

from user.views import register, MemberView, LoginView

urlpatterns = [
    url('^register/$', register, name='注册'),
    url('^login/$',  LoginView.as_view(), name='登录'),
    url(r'^member/$', MemberView.as_view(), name='个人中心'),
]
