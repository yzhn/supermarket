# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_name', models.CharField(max_length=50, verbose_name='活动产品')),
                ('activeImg', models.ImageField(upload_to='activeImg/%y%m/%d', verbose_name='活动商品相册')),
                ('url', models.CharField(max_length=100, verbose_name='活动产品地址')),
            ],
            options={
                'verbose_name': '活动表',
                'verbose_name_plural': '活动表',
                'db_table': 'Active',
            },
        ),
        migrations.CreateModel(
            name='ActivityArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_name', models.CharField(max_length=100, verbose_name='活动专区产品名称')),
                ('describe', models.TextField(blank=True, null=True, verbose_name='产品描述')),
                ('order', models.SmallIntegerField(default=0, verbose_name='轮播排序')),
                ('helves', models.SmallIntegerField(choices=[('下架', 0), ('上架', 1)], default=1, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '活动专区表',
                'verbose_name_plural': '活动专区表',
                'db_table': 'ActivityArea',
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel_name', models.CharField(max_length=50, verbose_name='商品名')),
                ('shopImg', models.ImageField(upload_to='shopImg/%y%m/%d', verbose_name='商品相册')),
                ('order', models.SmallIntegerField(default=0, verbose_name='轮播排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '轮播表',
                'verbose_name_plural': '轮播表',
                'db_table': 'Carousel',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_address', models.CharField(max_length=100, verbose_name='图片地址')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '商品相册表',
                'verbose_name_plural': '商品相册表',
                'db_table': 'Photo',
            },
        ),
        migrations.CreateModel(
            name='ShopClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cla_name', models.CharField(max_length=30, verbose_name='分类名')),
                ('class_intro', models.CharField(blank=True, max_length=200, null=True, verbose_name='分类介绍')),
                ('order', models.SmallIntegerField(default=0, verbose_name='商品分类排序')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'db_table': 'ShopClass',
            },
        ),
        migrations.CreateModel(
            name='ShopSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=50, verbose_name='商品名')),
                ('shop_brief', models.CharField(blank=True, max_length=100, null=True, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='价格')),
                ('stock', models.PositiveIntegerField(blank=True, null=True, verbose_name='库存')),
                ('sales', models.PositiveIntegerField(blank=True, null=True, verbose_name='销量')),
                ('shop_logo', models.ImageField(upload_to='shop_logo/%y%m/%d', verbose_name='商品logo')),
                ('shelves', models.SmallIntegerField(choices=[('下架', 0), ('上架', 1)], default=1, verbose_name='是否上架')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('ShopClass_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopClass', verbose_name='商品分类ID')),
            ],
            options={
                'verbose_name': '商品SKU表',
                'verbose_name_plural': '商品SKU表',
                'db_table': 'ShopSKU',
            },
        ),
        migrations.CreateModel(
            name='ShopSPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=30, verbose_name='商品名')),
                ('shop_detail', models.TextField(blank=True, null=True, verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU表',
                'verbose_name_plural': '商品SPU表',
                'db_table': 'ShopSPU',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '商品单位表',
                'verbose_name_plural': '商品单位表',
                'db_table': 'Unit',
            },
        ),
        migrations.AddField(
            model_name='shopsku',
            name='spu_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopSPU', verbose_name='商品spu_id'),
        ),
        migrations.AddField(
            model_name='shopsku',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Unit', verbose_name='单位'),
        ),
        migrations.AddField(
            model_name='photo',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopSKU', verbose_name='商品sku_id'),
        ),
        migrations.AddField(
            model_name='carousel',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopSKU', verbose_name='商品sku_id'),
        ),
        migrations.AddField(
            model_name='activityarea',
            name='sku_id',
            field=models.ManyToManyField(to='shop.ShopSKU', verbose_name='商品shu_id'),
        ),
    ]
