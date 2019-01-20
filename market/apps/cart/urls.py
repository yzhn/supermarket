from django.conf.urls import url

from cart.views import collect

urlpatterns = [
    url('^collect/$', collect, name='收藏'),
    # url('^login/$', login, name='登录'),
]
