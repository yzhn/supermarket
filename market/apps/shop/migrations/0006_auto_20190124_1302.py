# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-24 13:02
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20190123_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='ph_address',
            field=models.ImageField(upload_to='ph_address/%y%m/%d', verbose_name='图片地址'),
        ),
        migrations.AlterField(
            model_name='shopspu',
            name='shop_detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='商品详情'),
        ),
    ]
