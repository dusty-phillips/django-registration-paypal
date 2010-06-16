# Edited version of the django_registration defaultbackend
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.forms import RegistrationForm
from paypal_registration.models import RegistrationProfile


class PaypalBackend(object):
    """
    A registration backend which requires payment from paypal.
    The workflow is:

    1. User signs up for account.
    2. User is directed to paypal to pay for their account.
    3. Paypal notifies site that account has been paid for.
    4. User receives email containing instructions for activating the account.
    5. User activates and begins using the site.

    To use it:
    * ensure registration and paypal_registration are both in settings.py
        INSTALLED_APPS
    * run syncdb to install the paypal_registration model
    * create the normal django-registration templates (for the default backend) as well as:
        * registration/pay_with_paypal.html which shows a 'pay now' button.
             There is an example template in the app templates directory for
             this, but you should create your own.
        * registration/confirm_payment_received.html which is the template
             redirected to when paypal has processed payment and sends the user
             back to your site.

    """
    def register(self, request, **kwargs):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``paypal_registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account, and indicating that they are unpaid.

        The user will be redirected to a paypal payment selection page.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        
        """
        activated = RegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)
        return activated

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.
        
        """
        return RegistrationForm

    def post_registration_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('pay_with_paypal', (user.username,), {})

    def post_activation_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        account activation.
        
        """
        return ('registration_activation_complete', (), {})
