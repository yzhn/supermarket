from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from cart.helper import json_msg, get_cart_count
from db.base_view import VerifyLoginView
from shop.models import ShopSKU


def collect(request):
    return render(request, 'cart/collect.html')


# 添加购物车
class AddCartView(VerifyLoginView):
    def post(self, request):
        # 接受参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 判断id和数量是否为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, '参数错误'))
        # 要在数据库中存在商品
        try:
            shop_sku = ShopSKU.objects.get(pk=sku_id)
        except ShopSKU.DoesNotExist:

            return JsonResponse(json_msg(2, '商品不存在'))
        #         判断库存
        if shop_sku.stock < count:
            return JsonResponse(json_msg(3, '库存不足'))
        #         操作数据库
        r = get_redis_connection()
        #         处理key
        cart_key = f'cart_{user_id}'
        # 获取购物车中的数量加上需要的数量与库存作比较
        # 是二进制
        old_count = r.hget(cart_key, sku_id)
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)
        if shop_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, '库存不足'))
        #         添加购物车
        r.hincrby(cart_key, sku_id, count)
        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        return JsonResponse(json_msg(0, '添加购物车成功', data=cart_count))


# 购物车展示
class ShowCartView(VerifyLoginView):
    def get(self, request):
        user_id = request.session.get('ID')
        r = get_redis_connection()
        cart_key = f'cart_{user_id}'
        # 获取数据
        data = r.hgetall(cart_key)
        # 遍历字典
        cart_datas = []
        for sku_id, count in data.items():
            sku_id = int(sku_id)
            count = int(count)
            # 根据sku_id去找商品的信息
            shop_skus = ShopSKU.objects.get(pk=sku_id)
            # 绑定商品的数量
            shop_skus.count = count
            cart_datas.append(shop_skus)
        context = {'cart_datas': cart_datas}

        return render(request, 'cart/shopcart.html', context=context)
