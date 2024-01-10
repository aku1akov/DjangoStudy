from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _


def allowed_email(email):
    domains = ['@rt.ru', '@nw.rt.ru']
    if not any(domain in email for domain in domains):
        raise ValidationError(
            ('Указан некорректный домен для Email'),
            # params={'email': email}
        )
