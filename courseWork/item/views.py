from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from item.models  import Item, Order
from django.http import QueryDict, JsonResponse
from rest_framework import serializers
from django.core import serializers

def index_view(request):
    context = {
        'items': Item.objects.all(),
        'orders': Order.objects.all(),
    }
    return render(request, 'item/index.html', context)
  
@csrf_exempt
def order_items_api(request): 
    if request.method == "GET":
        data = Item.objects.all()
        serialized_object = serializers.serialize('python', data)
        return JsonResponse(serialized_object, safe=False)
    elif request.method == "POST":
        list_items = request.POST.getlist('arr[]') # get list of items
        order_num = request.POST.getlist('o_n') # get order num
        order_date = request.POST.getlist('o_d') # get order date 
        order = Order(num=order_num[0], date=order_date[0])
        order.save()
        order_id = order.id
        print(order_id)
        items = Item.objects.filter(name__in=list_items)
        order.items.add(*items)
        order = Order.objects.filter(num=order_num)
        return JsonResponse({'id' : order_id})
    else:
        return JsonResponse({'status' : 'Error'})


@csrf_exempt
def order_items_api_2(request, order_id):
    order = Order.objects.filter(id=order_id)
    if request.method == "GET":
        serialized_object = serializers.serialize('python', order)
        return JsonResponse(serialized_object, safe=False)
    elif request.method == "DELETE":
        order.delete()
        return JsonResponse({'status':'Deleted!'})
    elif  request.method == "PUT":
        data = QueryDict(request.body)
        item_list = data.getlist('arr[]')
        order_num = data.get('o_n')
        order_date = data.get('o_d')
        order_new = Order(order_id, order_num, order_date)
        order = order_new
        order.save()
        if(len(item_list) != 0):
            order.items.clear()
        for i in range(len(item_list)):
            item_name = item_list[i]
            item_temp = Item.objects.filter(name=item_name)
            order.items.add(*item_temp)
        return JsonResponse({'status' : 'Saved'})
    else:
        return JsonResponse({'status': 'Error'})


@csrf_exempt
def item_api_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if request.method == "DELETE":
            item.delete()
            return JsonResponse({
                'status':'Deleted!'
            })
        elif request.method == "PUT":
            put = QueryDict(request.body)
            name = put.get('n')
            price = put.get('p')
            shelfLife = False
            if(put.get('sl') == "on"):
                shelfLife = True
            new_item = Item(item_id,name,price,shelfLife)
            item = new_item
            item.save()
            return JsonResponse({'status' : 'Editing was successful'})
        elif request.method == "GET":
            data = Item.objects.filter(id=item_id)
            serialized_object = serializers.serialize('python', data)
            return JsonResponse(serialized_object, safe=False)
        return HttpResponseBadRequest("Invalid HTTP method")
    except Item.DoesNotExist:
        return HttpResponseBadRequest("Invalid item ID")

@csrf_exempt
def item_api_create(request):
    if(request.method == "POST"):
        put = QueryDict(request.body)
        name = put.get('n')
        price = put.get('p')
        shelfLife = False
        if(put.get('sl') == "on"):
            shelfLife = True
        new_item = Item.objects.create(name=name,price=price,shelfLife=shelfLife)
        print(new_item.id)
        return JsonResponse({'status' : 'Creating was successful', 'id' : new_item.id})
    else:
        return HttpResponseBadRequest("Invalid HTTP method")