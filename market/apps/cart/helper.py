from django_redis import get_redis_connection


def json_msg(code, msg=None, data=None):
    # 封装json的消息,code:0为正确,其他的都为错误
    return {'code': code, 'errmsg': msg, 'data': data}


# 获取当前用户购物车中的总数量
def get_cart_count(request):
    user_id = request.session.get('ID')
    if user_id is None:
        return 0
    else:
        r = get_redis_connection()
        cart_key = f'cart_{user_id}'
        values = r.hvals(cart_key)
        total_count = 0
        for v in values:
            total_count += int(v)
        return total_count
