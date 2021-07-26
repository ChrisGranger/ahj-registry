from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator
from .signals import *

from djoser.email import ActivationEmail
from djoser import utils
from djoser.conf import settings
import django.dispatch



class ActivateUserEmail(ActivationEmail):

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        activation_email_sent.send(sender=self.__class__, uid=context['uid'], token=context['token'])
        return context