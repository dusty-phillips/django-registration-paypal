from django.db import models
from registration.models import RegistrationProfile


class PaypalRegistrationProfile(RegistrationProfile):
    paid = models.BooleanField(default=False)
