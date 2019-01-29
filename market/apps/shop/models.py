from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
# 商品分类
# ID
# 分类名
# 分类简介
# 添加时间
# 修改时间
# 是否删除
class ShopClass(models.Model):
    cla_name = models.CharField(max_length=30, verbose_name='分类名')
    class_intro = models.CharField(max_length=200, verbose_name='分类介绍', null=True, blank=True)
    order = models.SmallIntegerField(default=0, verbose_name='商品分类排序')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cla_name

    class Meta:
        db_table = 'ShopClass'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


# 商品SPU表
# ID
# 名称
# 详情
class ShopSPU(models.Model):
    shop_name = models.CharField(max_length=30, verbose_name='商品名')
    shop_detail = RichTextUploadingField(verbose_name='商品详情', null=True, blank=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = 'ShopSPU'
        verbose_name = '商品SPU表'
        verbose_name_plural = verbose_name


# 商品单位表
# ID
# 单位名（斤，箱）
# 添加时间
# 修改时间
# 是否删除
class Unit(models.Model):
    unit_name = models.CharField(max_length=20, verbose_name='单位')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = 'Unit'
        verbose_name = '商品单位表'
        verbose_name_plural = verbose_name


# 商品SKU表
# ID
# 商品名
# 简介
# 价格
# 单位
# 库存
# 销量
# LOGO地址
# 是否上架
# 商品分类ID
# 商品spu_id
# 添加时间
# 修改时间
# 是否删除
class ShopSKU(models.Model):
    choices = ((0, '下架'), (1, '上架'))
    shop_name = models.CharField(max_length=50, verbose_name='商品名')
    shop_brief = models.CharField(max_length=100, null=True, blank=True, verbose_name='商品简介')
    # 价格（最高金额为10万，小数最多4个小数点）
    price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='价格')
    stock = models.PositiveIntegerField(verbose_name='库存', null=True, blank=True)
    # 销量
    sales = models.PositiveIntegerField(verbose_name='销量', null=True, blank=True)
    # LOGO地址
    shop_logo = models.ImageField(upload_to='shop_logo/%y%m/%d', verbose_name='商品logo')
    # 是否上架
    shelves = models.SmallIntegerField(choices=choices, default=1, verbose_name='是否上架')
    # 商品分类ID  外键  GoodsClassModel
    ShopClass_id = models.ForeignKey(to=ShopClass, verbose_name='商品分类ID')
    # 商品spu_id   外键  GoodsSPUModel
    spu_id = models.ForeignKey(to=ShopSPU, verbose_name='商品spu_id')
    # 单位 外键   UnitModel
    unit = models.ForeignKey(to=Unit, verbose_name='单位')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'ShopSKU'
        verbose_name = '商品SKU表'
        verbose_name_plural = verbose_name  # 复数名

    def __str__(self):
        return self.shop_name


# 商品相册
# ID
# 图片地址
# 商品SKUID
# 添加时间
# 修改时间
# 是否删除
class Photo(models.Model):
    ph_address = models.ImageField(upload_to='ph_address/%y%m/%d', verbose_name='图片地址')
    sku_id = models.ForeignKey(to=ShopSKU, verbose_name='商品sku_id')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '商品相册:{}'.format(self.ph_address.name)

    class Meta:
        db_table = 'Photo'
        verbose_name = '商品相册表'
        verbose_name_plural = verbose_name


# 首页轮播商品
# ID
# 名称
# 商品SKUID
# 图片地址
# 排序（order）
# 添加时间
# 修改时间
# 是否删除

class Carousel(models.Model):
    carousel_name = models.CharField(max_length=50, verbose_name='商品名')
    sku_id = models.ForeignKey(to=ShopSKU, verbose_name='商品sku_id')
    shopImg = models.ImageField(upload_to='shopImg/%y%m/%d', verbose_name='商品相册')
    # 排序（order）
    order = models.SmallIntegerField(default=0, verbose_name='轮播排序')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.carousel_name

    class Meta:
        db_table = 'Carousel'
        verbose_name = '轮播表'
        verbose_name_plural = verbose_name


# 首页活动表
# ID
# 名称
# 图片地址
# url地址/SKUID
class Active(models.Model):
    active_name = models.CharField(max_length=50, verbose_name='活动产品')
    activeImg = models.ImageField(upload_to='activeImg/%y%m/%d', verbose_name='活动商品相册')
    url = models.CharField(max_length=100, verbose_name='活动产品地址')

    def __str__(self):
        return self.active_name

    class Meta:
        db_table = 'Active'
        verbose_name = '活动表'
        verbose_name_plural = verbose_name


# 首页活动专区
# ID
# 名称
# 描述
# 排序
# skuid __ manytomanyfield
# 是否上架
# 添加时间
# 修改时间
# 是否删除

class ActivityArea(models.Model):
    choices = ((0, '下架'), (1, '上架'))
    act_name = models.CharField(max_length=100, verbose_name='活动专区产品名称')
    describe = models.TextField(null=True, blank=True, verbose_name='产品描述')
    order = models.SmallIntegerField(default=0, verbose_name='轮播排序')
    sku_id = models.ManyToManyField(to=ShopSKU, verbose_name='商品shu_id')
    helves = models.SmallIntegerField(choices=choices, default=1, verbose_name='是否上架')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.act_name

    class Meta:
        db_table = 'ActivityArea'
        verbose_name = '活动专区表'
        verbose_name_plural = verbose_name
