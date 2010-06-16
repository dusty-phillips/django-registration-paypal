from django.db import models
from registration.models import RegistrationProfile, RegistrationManager


class PaypalRegistrationProfile(RegistrationProfile):
    paid = models.BooleanField(default=False)
    objects = RegistrationManager()
