from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,13}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed."
)
