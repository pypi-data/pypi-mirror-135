from django.core.mail import send_mail


class ConfirmationEmail:
    """
    A confirmation email message
    """

    subject = ""

    def __init__(self, email):
        self.email = email

    def get_subject(self):
        return self.subject

    def get_body(self, **kwargs) -> str:
        """Returns the body of the email message.

        :param kwargs: contains at least the keys "instance", "pk" and "token"
        :return: a string with the body of the email message
        """
        return ""

    def send(self, **kwargs):
        send_mail(
            self.get_subject(),
            self.get_body(**kwargs),
            from_email=None,
            recipient_list=[self.email],
        )
