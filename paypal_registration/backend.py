from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.forms import RegistrationForm
from registration.backends.default import DefaultBackend
from paypal_registration.models import PaypalRegistrationProfile


class PaypalBackend(DefaultBackend):
    """
    A registration backend which requires payment from paypal before the
    account can be activated.
    The workflow is:

    1. User signs up for account.
    2. User is directed to paypal to pay for their account.
    3. Paypal notifies site that account has been paid for.
    4. User receives email containing instructions for activating the account.
    5. User activates and begins using the site.

    To use it:
    * ensure registration and paypal_registration are both in settings.py
        INSTALLED_APPS
    * add a PAYPAL_ID setting to settings.py. This can be either the e-mail
        address associated with your paypal seller account, or the secure
        ID paypal assigns. You can get this id by checking the unencrypted form
        code for a buy it now button you create on site.
    * add a USE_PAYPAL_SANDBOX boolean setting to settings.py. This can be used
         for testing. See developer.paypal.com for details. This value is set
         to *True* by default, which means you have to explicitly set it to
         False in production instances.
    * run syncdb to install the paypal_registration model
    * ensure the sites model is correctly set up for your site in the django
         admin. It is used to construct the paypal IPN url, so make sure it's
         correct.
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
        ``paypal_registration.models.PaypalRegistrationProfile`` will be
        created, tied to that ``User``, containing the activation key which
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
        new_user = PaypalRegistrationProfile.objects.create_inactive_user(username,
                email, password, site, send_email=False)
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
        activated = PaypalRegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)
        return activated

    def post_registration_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('pay_with_paypal', (user.username,), {})
