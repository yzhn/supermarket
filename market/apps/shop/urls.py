from django.conf.urls import url

from shop.views import index, detail, category

urlpatterns = [
    url('^index/$', index, name='首页'),
    url('^category/(?P<cate_id>\d+)_?(?P<>\d+)$', category, name='商品分类'),
    url(r'^detail/(?P<id>\d+)/$', detail, name="详情"),
]
