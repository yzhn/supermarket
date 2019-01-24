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


'''排序时传入参数order对综合,销量,价格,时间进行排序
orderrule=[]'''


def category(request, cate_id, order):
    # 查询所有的商品分类
    shop_class = ShopClass.objects.filter(is_delete=False).order_by(-order)
    # 查询所有的商品信息
    shop_class = shop_class[0]
    shop_sku = ShopSKU.objects.filter(is_delete=False, ShopClass_id=shop_class)
    context = {'shop_class': shop_class,
               'shop_sku': shop_sku,
               'order': order,
               'id': id, }

    return render(request, 'shop/category.html', context=context)
