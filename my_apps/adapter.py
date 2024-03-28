"""
An adapter is a design pattern that allows you to modify or extend the behavior of a
class or a function without modifying its structure.
"""
from django.core.mail import send_mail


#########################################################################################
# Function Adapter
def send_email(subject, message, recipient_list):
    send_mail(subject, message, 'noreply@example.com', recipient_list)


def send_email_with_logging(subject, message, recipient_list):
    """
    It is a send_email function's adapter, which can run some logic after or before send_email runs.
    """
    print('before')
    send_email(subject, message, recipient_list)
    print('after')


#########################################################################################
# Class Adapter
class EmailService:
    @staticmethod
    def send_email(subject, message, recipient_list):
        send_mail(subject, message, 'noreply@example.com', recipient_list)


class EmailServiceAdapter(EmailService):
    def send_email_with_logging(self, subject, message, recipient_list):
        """
        It is a send_email function's adapter, which can run some logic after or before send_email runs.
        """
        print('before')
        self.send_email(subject, message, recipient_list)
        print('after')
