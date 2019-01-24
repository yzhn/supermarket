from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from shop.models import ShopSPU, ShopSKU, ShopClass


def index(request):
    return render(request, 'shop/index.html')


def detail(request, id):
    # 获取商品的shopsku信息
    shop_sku = ShopSKU.objects.get(pk=id)
    context = {'shop_sku': shop_sku}
    return render(request, 'shop/detail.html', context=context)


def category(request):
    # 查询所有的商品分类
    shop_class = ShopClass.objects.filter(is_delete=False)
    # 查询所有的商品信息
    shop_sku = ShopSKU.objects.filter(is_delete=False)
    context = {'shop_class': shop_class,
               'shop_sku': shop_sku}

    return render(request, 'shop/category.html', context=context)
