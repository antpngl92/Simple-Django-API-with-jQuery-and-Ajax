from django.contrib import admin
from django.urls import path, include

from .views import index_view, item_api_item,item_api_create, order_items_api,order_items_api_2

urlpatterns = [
    path('', index_view, name="index"),
    path('api/item/<int:item_id>/', item_api_item, name="item api"),
    path('api/item/', item_api_create, name="item create api"),
    path('api/order/item-list/', order_items_api, name="order-items api"),
    path('api/order/item-list/<int:order_id>/', order_items_api_2, name="order-item api"),
]
