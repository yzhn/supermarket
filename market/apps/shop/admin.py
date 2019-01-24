from django.contrib import admin

# Register your models here.
from shop.models import ShopClass, ShopSPU, Unit, ShopSKU, Photo, Carousel, Active, ActivityArea

admin.site.register(ShopClass)
admin.site.register(ShopSPU)
admin.site.register(Unit)
admin.site.register(ShopSKU)
admin.site.register(Photo)
admin.site.register(Carousel)
admin.site.register(Active)
admin.site.register(ActivityArea)
