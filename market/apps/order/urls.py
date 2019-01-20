from django.conf.urls import url

from order.views import all_order

urlpatterns = [
    url('^all_order/$', all_order, name='所有订单'),

]
