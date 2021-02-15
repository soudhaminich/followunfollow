from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import requires_csrf_token
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from support.models import Order


# @requires_csrf_token
# def handler404(request, *args, **kwargs):
#     return redirect('index')


def handle_payment(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj.__dict__)
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        if (ipn_obj.receiver_email != settings.PAYPAL_ACCOUNT or
                ipn_obj.mc_currency != 'USD'):
            # Not a valid payment
            return

        try:
            order = Order.objects.get(
                pk=ipn_obj.invoice[len(settings.PAYPAL_PREFIX):],
                amount=ipn_obj.mc_gross
            )
        except Order.DoesNotExist:
            return

        order.payment_id = ipn_obj.txn_id
        order.payment_email = ipn_obj.payer_email
        order.save()

        question = order.question

        question.priority = question.priority[0]
        question.approved = 'Y'
        question.save()
    else:
        pass
        # handle other status


valid_ipn_received.connect(handle_payment)
