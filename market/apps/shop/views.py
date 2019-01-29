from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.helper import get_cart_count
from shop.models import ShopSKU, ShopClass, ActivityArea


def index(request):
    act_areas = ActivityArea.objects.filter()
    context = {'act_areas': act_areas}

    return render(request, 'shop/index.html', context=context)


def detail(request, id):
    # 获取商品的shopsku信息
    shop_sku = ShopSKU.objects.get(pk=id)
    context = {'shop_sku': shop_sku}
    return render(request, 'shop/detail.html', context=context)


'''排序时传入参数order对综合,销量,价格,时间进行排序
orderrule=[]'''


def category(request, id, order):
    # 查询所有的商品分类
    shop_classes = ShopClass.objects.filter(is_delete=False).order_by('-order')
    # 查询所有的商品信息

    if id == "":
        shop_class = shop_classes[0]
        id = shop_class.pk
    else:
        # 根据分类id查询对应的分类
        id = int(id)
        shop_class = ShopClass.objects.get(pk=id)
    # 查询对应类下的所有商品
    shop_skus = ShopSKU.objects.filter(is_delete=False, ShopClass_id=shop_class)
    if order == "":
        order = 0
    order = int(order)

    # 排序规则列表
    order_rule = ['pk', '-sales', 'price', '-price', '-add_time']
    shop_skus = shop_skus.order_by(order_rule[order])
    # 获取当前用户购物车的总数量
    cart_count = get_cart_count(request)
    context = {'shop_classes': shop_classes,
               'shop_skus': shop_skus,
               'order': order,
               'id': id,
               'cart_count': cart_count, }

    return render(request, 'shop/category.html', context=context)
