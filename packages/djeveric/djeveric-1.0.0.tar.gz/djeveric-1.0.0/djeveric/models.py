from typing import Any, Iterable, Mapping

from djeveric.fields import ConfirmationField
from djeveric.tokens import ConfirmationTokenGeneratorProxy


class ConfirmableModelMixin:
    """
    Mixin for models which can be confirmed via email.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confirmation_token_generator_proxy = ConfirmationTokenGeneratorProxy(self)

    def confirm(self) -> None:
        """
        Confirms the model instance.
        """
        setattr(self, self._get_confirmation_field().name, True)
        self.save()

    def get_confirmation_email_kwargs(self) -> Mapping[str, Any]:
        return {
            "instance": self,
            "pk": self.pk,
            "token": self.make_confirmation_token(),
        }

    def get_confirmation_email_recipient(self) -> str:
        """
        Returns the email address where to send the confirmation email.

        :return: a string containing an email address
        """
        try:
            return self.email
        except AttributeError as exc:
            raise NotImplementedError(
                f"You should implement get_confirmation_email_recipient in {self.__class__.__name__}."
            ) from exc

    def check_confirmation_token(self, token):
        return self.confirmation_token_generator_proxy.check_token(token)

    def get_confirmation_token_data(self) -> Iterable[str]:
        """
        Returns the data on which confirmation token generation is based. The data is converted to strings and hashed
        with a salt.

        The data should
        - differentiate the model instance (e.g. by using the pk) and
        - change on confirmation of the model instance.

        :return: a list of data items
        """
        return [
            str(self.pk),
            self.get_confirmation_email_recipient(),
            str(self._is_confirmed()),
        ]

    def make_confirmation_token(self):
        return self.confirmation_token_generator_proxy.make_token()

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self._is_confirmed() and self._has_confirmation_recipient():
            self._send_request()

    def _get_confirmation_field(self):
        for field in self._meta.get_fields(False, False):
            if isinstance(field, ConfirmationField):
                return field
        raise NotImplementedError(
            f"You must specify a ConfirmationField on {self.__class__.__name__}."
        )

    def _get_confirmation_email(self):
        return self._get_confirmation_field().confirmation_email_class(
            self.get_confirmation_email_recipient()
        )

    def _has_confirmation_recipient(self):
        """Returns True if a confirmation request can be sent."""
        return True

    def _is_confirmed(self) -> bool:
        return getattr(self, self._get_confirmation_field().name)

    def _send_request(self):
        assert not self._is_confirmed()
        message = self._get_confirmation_email()
        kwargs = self.get_confirmation_email_kwargs()
        message.send(**kwargs)
