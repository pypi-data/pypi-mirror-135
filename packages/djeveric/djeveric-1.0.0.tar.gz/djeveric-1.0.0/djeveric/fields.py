from django.db import models

from djeveric.emails import ConfirmationEmail


class ConfirmationField(models.BooleanField):
    def __init__(self, **kwargs):
        self.confirmation_email_class = kwargs.pop("email_class", ConfirmationEmail)
        kwargs["default"] = False
        super().__init__(**kwargs)
