from django.conf.urls import url

from shop.views import index

urlpatterns = [
    url('^index/$', index, name='首页'),
    # url('^login/$', login, name='登录'),
]
