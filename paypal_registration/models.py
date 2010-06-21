from django.db import models
from registration.models import RegistrationProfile, RegistrationManager

class PaypalRegistrationManager(RegistrationManager):

    def activate_user(self, activation_key):
        try:
            profile = self.get(activation_key=activation_key, paid=True)
        except self.model.DoesNotExist:
            return False

        return super(PaypalRegistrationManager, self).activate_user(activation_key)

class PaypalRegistrationProfile(RegistrationProfile):
    paid = models.BooleanField(default=False)
    objects = PaypalRegistrationManager()

