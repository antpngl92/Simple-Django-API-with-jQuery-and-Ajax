from django.contrib import admin

from item.models import Item, Order

# Register your models here.



class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'shelfLife')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','num','date')

admin.site.register(Item, ItemAdmin)    
admin.site.register(Order, OrderAdmin)