from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def pay_with_paypal(request, username):
    paypal_id = settings.PAYPAL_ID
    use_sandbox = getattr(settings, "USE_PAYPAL_SANDBOX", True)

    return render_to_response("registration/pay_with_paypal.html",
            RequestContext(request,
                {'paypal_id': paypal_id,
                    'use_sandbox': use_sandbox}))
