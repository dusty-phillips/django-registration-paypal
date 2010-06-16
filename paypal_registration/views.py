from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt

from paypal_registration.models import PaypalRegistrationProfile

def pay_with_paypal(request, username):
    user = get_object_or_404(User, username=username)
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
                    'return_url': return_url,
                    'item_number': username}))

@csrf_exempt
def paypal_instant_notify(request):
    # FIXME: Some validation here (ie: that it really came from paypal) is
    # absolutely essential
    username = request.POST['item_number']
    profiles = PaypalRegistrationProfile.objects.filter(user__username=username)
    profiles.update(paid=True)

    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    profiles[0].send_activation_email(site)

    return HttpResponse("ACK")
