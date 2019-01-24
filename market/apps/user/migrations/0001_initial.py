# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 19:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机号码格式错误')], verbose_name='手机号码')),
                ('nickname', models.CharField(blank=True, max_length=30, null=True, verbose_name='昵称')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('gender', models.SmallIntegerField(choices=[('男', 1), ('女', 2)], default=1, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('school', models.CharField(blank=True, max_length=30, null=True, verbose_name='学校')),
                ('hometown', models.CharField(blank=True, max_length=30, null=True, verbose_name='地址')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('logo', models.ImageField(default='head/1547797692997.jpg', upload_to='head/%Y%m/%d', verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
                'db_table': 'Register',
            },
        ),
    ]
