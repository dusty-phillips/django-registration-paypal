==================================
Django Registration Paypal Backend
==================================

This is a django-registration backend to integrate with paypal. The workflow is
as follows:

1. User signs up for account.
2. User is directed to paypal to pay for their account.
3. Paypal notifies site that account has been paid for.
4. User receives email containing instructions for activating the account.
5. User activates and begins using the site.

This is a backend for the django-registration project:
http://bitbucket.org/ubernostrum/django-registration/
It requires the development version of django-registration; 0.7 did not support
registration backends.

This code uses paypal's standard integration. It posts to an Instant Payment
Notification URL when complete.
