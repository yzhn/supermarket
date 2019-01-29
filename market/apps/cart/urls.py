from django.conf.urls import url

from cart.views import collect, AddCartView, ShowCartView

urlpatterns = [
    url('^collect/$', collect, name='收藏'),
    url('^add/$', AddCartView.as_view(), name='添加购物车'),
    url('^show/$', ShowCartView.as_view(), name='展示购物车'),
]
