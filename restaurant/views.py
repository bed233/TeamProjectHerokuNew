from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime

from customer.models import OrderModel
from restaurant.models import DashboardModel


# Dashboard View send and receives data from the Database to and from the rendered HTML.
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month,
                                           created_on__day=today.day)
        table = DashboardModel.objects.get(pk=1)

        table_not_cancelled_orders = []

        for order in orders:
            if table.selected_table_number == 0:
                table_not_cancelled_orders.append(order)  # Shows all orders if table number is set to 0
            elif order.table_number == table.selected_table_number:  # Filter orders to only show orders that match
                # table_number
                table_not_cancelled_orders.append(order)

        for orders in table_not_cancelled_orders:
            if orders.is_cancelled:
                table_not_cancelled_orders.remove(orders)

        total_revenue = 0
        for order in table_not_cancelled_orders:
            total_revenue += order.price

        context = {  # Passed to HTML in order to be able to acccess data.
            'orders': reversed(table_not_cancelled_orders),
            'total_revenue': total_revenue,
            'total_orders': len(table_not_cancelled_orders),
        }

        return render(request, 'restaurant/dashboard.html',
                      context)  # Render HTML file for Dashboard along with context set

    def post(self, request, *args, **kwargs):
        table = DashboardModel.objects.get(pk=1)
        table_number = request.POST.get("table_number")  # Retrieves currently selected Table number from Site.

        if table_number is None:
            table_number = 0

        table.selected_table_number = table_number
        table.save()

        return redirect('dashboard')

# Shows staff indepth description of selected order.
class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'order': order,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        if 'Confirm' in request.POST:  # Checks if confirm order button has been pressed.
            order.order_confirmed = True
            order.save()
        elif 'Delivered' in request.POST:  # Checks if Order delivered button has been pressed.
            order.is_delivered = True
            order.save()
        elif 'ReadyDeliver' in request.POST:  # Checks if Ready to be delivered button has been pressed.
            order.ready_to_deliver = True
            order.save()
        elif 'Cancel' in request.POST:  # Checks if order has been cancelled by Staff
            order.is_cancelled = True
            order.save()
            return redirect('dashboard')

        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
