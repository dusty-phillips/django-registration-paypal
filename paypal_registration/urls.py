"""
URLconf for registration and activation, using the paypal_registration backend

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),
"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt

from registration.views import activate
from registration.views import register


urlpatterns = patterns('',
   url(r'^activate/complete/$',
       direct_to_template,
       {'template': 'registration/activation_complete.html'},
       name='registration_activation_complete'),
   url(r'^activate/(?P<activation_key>\w+)/$',
       activate,
       {'backend': 'paypal_registration.backend.PaypalBackend'},
       name='registration_activate'),
   url(r'^register/$',
       register,
       {'backend': 'paypal_registration.backend.PaypalBackend'},
       name='registration_register'),
   url(r'^register/complete/$',
       direct_to_template,
       {'template': 'registration/registration_complete.html'},
       name='registration_complete'),
   url(r'^register/closed/$',
       direct_to_template,
       {'template': 'registration/registration_closed.html'},
       name='registration_disallowed'),
   url(r'^pay_with_paypal/(?P<username>\w+)/$',
       'paypal_registration.views.pay_with_paypal',
       name='pay_with_paypal'),
   url(r'^payment_confirmation/$',
       csrf_exempt(direct_to_template),
       {'template': 'registration/confirm_payment_received.html'},
       name="confirm_payment_received"),
   url(r'^paypal_IPN_notify/$',
       'paypal_registration.views.paypal_instant_notify',
       name='paypal_notify'),
   (r'', include('registration.auth_urls')),
   )
