from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        token = six.text_type(user.pk)+ six.text_type(timestamp)+ six.text_type(user.is_active)
        return token

account_activation_token=AccountActivationTokenGenerator()