from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Register(models.Model):
    choices = ((1, '男'), (2, '女'))
    phone = models.CharField(max_length=11,
                             verbose_name='手机号码',
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')])
    nickname = models.CharField(max_length=30, null=True, blank=True, verbose_name='昵称')
    password = models.CharField(max_length=32, verbose_name='密码')
    gender = models.SmallIntegerField(choices=choices, default=1, verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')

    school = models.CharField(max_length=30, null=True, blank=True, verbose_name='学校')
    hometown = models.CharField(max_length=30, null=True, blank=True, verbose_name='地址')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    logo = models.ImageField(upload_to='head/%Y%m/%d', default='head/1547797692997.jpg', verbose_name='头像')

    def __str__(self):
        return self.phone

    class Meta:
        db_table = 'Register'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


class UserAddress(models.Model):
    """用户收货地址管理"""
    user = models.ForeignKey(to="Register", verbose_name="创建人")
    username = models.CharField(verbose_name="收货人", max_length=100)
    phone = models.CharField(verbose_name="收货人电话", max_length=11,
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')])
    hcity = models.CharField(verbose_name="省", max_length=100)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, default='')
    harea = models.CharField(verbose_name="区", max_length=100, blank=True, default='')
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
