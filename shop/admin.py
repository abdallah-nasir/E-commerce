from django.contrib import admin
from .models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=("user","device","ordered")
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Colors)
admin.site.register(Brands)
admin.site.register(OrderProduct,OrderAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(WishList)
admin.site.register(Coupon)
admin.site.register(final_order)
