from django.urls import path
from .views import Dashboard, OrderDetails
# path routes urls to the appropriate view function
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>', OrderDetails.as_view(), name='order-details')
]