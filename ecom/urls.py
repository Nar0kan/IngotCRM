from django.urls import path
from . import views


app_name = 'ecom'

urlpatterns = [
    path('order_page/<int:id>/<str:level_name>', views.orderPage, name='order_page'),
    path('paypal_return/', views.paypal_return, name='paypal-return'),
    path('paypal_cancel/', views.paypal_cancel, name='paypal-cancel'),
    path('order_complete/', views.orderCompletePage, name='order_complete'),
    path('order_incomplete/', views.orderIncompletePage, name='order_incomplete'),
]
