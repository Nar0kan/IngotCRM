import uuid

from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm

from leads.models import User


def orderPage(request, id, level_name):
    org = User.objects.get(id=id)
    host = request.get_host()
    level_name = level_name

    if level_name == "silver":
        price='24.99'
        team_size = 20
    elif level_name == "gold":
        price='49.99'
        team_size = 50

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': price,
        'item_name': f'Order {org}',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("ecom:paypal-return")}',
        'cancel_return': f'http://{host}{reverse("ecom:paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'user': org, 'form': form,
               'level_name': level_name.capitalize(), 'price': price}
    return render(request, 'order_page.html', context)


def paypal_return(request, **kwargs):
    return redirect('ecom:order_complete')


def paypal_cancel(request):
    messages.error(request, 'Your order has been cancelled!')
    return redirect('ecom:order_incomplete')


def orderCompletePage(request, **kwargs):
    return render(request, 'order_complete.html', context={})

def orderIncompletePage(request):
    return render(request, 'order_incomplete.html', {})
