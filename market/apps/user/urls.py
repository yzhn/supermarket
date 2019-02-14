from django.conf.urls import url

from user.views import register, MemberView, LoginView, forget_password, InforView, revise, SendMsm, AddressView, \
    Addresslist, AddressAddView, AddressEditView, delAddress

urlpatterns = [
    url('^register/$', register, name='注册'),
    url('^forget_password/$', forget_password, name='忘记密码'),
    url('^revise/$', revise, name='修改密码'),
    url('^login/$',  LoginView.as_view(), name='登录'),
    url(r'^member/$', MemberView.as_view(), name='个人中心'),
    url(r'^infor/$', InforView.as_view(), name='个人资料'),
    url(r'^sendMsm/$', SendMsm.as_view(), name='验证码'),
    url(r'^add/$', AddressView.as_view(), name='添加地址'),
    url(r'^addresslist/$', Addresslist.as_view(), name='地址列表'),
    url(r'^addressadd/$', AddressAddView.as_view(), name="address_add"),  # 收货地址添加
    url(r'^addressedit/(?P<id>\d+)/$', AddressEditView.as_view(), name="address_edit"),  # 收货地址编辑
    url(r'^addressdel/$', delAddress, name="address_del"),  # 收货地址删除

]
