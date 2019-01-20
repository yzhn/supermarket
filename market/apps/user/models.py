from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Register(models.Model):
    choices = (('男', 1), ('女', 2))
    phone = models.SmallIntegerField(max_length=11,
                                     verbose_name='手机号码',
                                     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')])
    nickname = models.CharField(max_length=30, null=True, blank=True, verbose_name='昵称')
    password = models.CharField(max_length=32, verbose_name='密码')
    gender = models.SmallIntegerField(choices=choices, default=1, verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')

    school = models.CharField(max_length=30, null=True, blank=True, verbose_name='学校')
    hometown = models.CharField(max_length=30, null=True, blank=True, verbose_name='地址')
    add_time = models.DateTimeField(null=True, blank=True, )
    mod_time = models.DateTimeField(null=True, blank=True)

    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.phone

    class Meta:
        db_table = 'Register'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
