from django.conf.urls import url

from user.views import register, login

urlpatterns = [
    url('^register/$', register, name='注册'),
    url('^login/$', login, name='登录'),
]
