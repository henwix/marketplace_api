from django.core.validators import RegexValidator

user_phone_validator = RegexValidator(
    regex=r'^\+?\d{9,20}$',
    message='The phone number must be in the format: +999999999, and the maximum length is 20',
)
