from django.conf.urls import url

from order.views import ConfirmOrder, ShowOrder, PayOrder

urlpatterns = [
    url(r'^confirm/$', ConfirmOrder.as_view(), name='确认订单'),
    url(r'^order/$', ShowOrder.as_view(), name='确认支付'),
    url(r'^payorder/$', PayOrder.as_view(), name='支付'),
]
