from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt

def pay_with_paypal(request, username):
    paypal_id = settings.PAYPAL_ID
    use_sandbox = getattr(settings, "USE_PAYPAL_SANDBOX", True)
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    paypal_ipn =  "http://%s%s" % (site.domain, reverse('paypal_notify'))
    return_url = "http://%s%s" % (site.domain, reverse('confirm_payment_received'))

    return render_to_response("registration/pay_with_paypal.html",
            RequestContext(request,
                {'paypal_id': paypal_id,
                    'use_sandbox': use_sandbox,
                    'notify_url': paypal_ipn,
                    'return_url': return_url}))

@csrf_exempt
def paypal_instant_notify(request):
    # FIXME: Some validation here is absolutely essential
    print("\n\n\nPAYPAL SAID YES\n\n\n")
    return HttpResponse("ACK")
