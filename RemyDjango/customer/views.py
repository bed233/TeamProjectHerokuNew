import json

from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, Allergy
from django.db.models import Q


# Index inherits from the views class
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')  # renders a html template


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


# For every order the primary key will be in the url
# we can get the current object to find each order
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order,
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }
        orderId = self.request.GET.get('orderId', '')
        email = self.request.GET.get('email', '')

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'order': order
        }

        if 'NeedHelp' in request.POST:
            order.need_help = True
            order.save()
            return redirect('order-confirmation', pk=order.pk)

        data = json.loads(request.body)

        if data['isPaid']:
            order.is_paid = True
            order.save()
            return redirect('order-confirmation', pk=order.pk)


# gets query from url using 'q'.
# Uses imported Q object to specify what we can search for through filtering.
# Q 'enscapulates an SQL expression in a python object that can be used in database-related operations'
class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        tacos = MenuItem.objects.filter(category__name__contains='Tacos').filter(Q(name__contains=query) |
                                                                                 Q(price__contains=query))
        burrito = MenuItem.objects.filter(
            category__name__contains='Burritos').filter(Q(name__contains=query) |
                                                        Q(price__contains=query))
        desserts = MenuItem.objects.filter(category__name__contains='Dessert').filter(Q(name__contains=query) |
                                                                                      Q(price__contains=query))
        nachos = MenuItem.objects.filter(category__name__contains='Nachos').filter(Q(name__contains=query) |
                                                                                   Q(price__contains=query))

        context = {
            'tacos': tacos,
            'burrito': burrito,
            'desserts': desserts,
            'nachos': nachos,
        }
        return render(request, 'customer/new_menu.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        table_number = request.POST.get('table_number')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')  # gets items and makes a list

        # loops through items and collects necessary data
        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)  # appends data to list

            price = 0
            item_ids = []
        # loops through items in order_items array and adds price to current price and appends ID into item_ids list
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            table_number=table_number
        )
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class NewMenu(View):
    def get(self, request, *args, **kwargs):
        tacos = MenuItem.objects.filter(category__name__contains='Tacos')
        burrito = MenuItem.objects.filter(
            category__name__contains='Burritos')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        nachos = MenuItem.objects.filter(category__name__contains='Nachos')

        context = {
            'tacos': tacos,
            'burrito': burrito,
            'desserts': desserts,
            'nachos': nachos,
        }
        return render(request, 'customer/new_menu.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        table_number = request.POST.get('table_number')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')  # gets items and makes a list

        # loops through items and collects necessary data
        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)  # appends data to list

            price = 0
            item_ids = []
        # loops through items in order_items array and adds price to current price and appends ID into item_ids list
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            table_number=table_number
        )
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)
