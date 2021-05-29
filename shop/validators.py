
from django.contrib.auth.validators import ASCIIUsernameValidator

custom_username_validators = [ASCIIUsernameValidator()]

# In settings.py

ACCOUNT_USERNAME_VALIDATORS = 'some.module.validators.custom_username_validators'