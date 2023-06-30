
from django import forms
from django.core.exceptions import ValidationError


def is_cabinet_office_email(email_address):
    # quick and dirty test
    # we don't care if is is a real email address as long as it looks near
    # enough.
    if not email_address.endswith('@cabinetoffice.gov.uk'):
        raise ValidationError('Must be a Cabinet Office email address')
    return True


class FeedbackForm(forms.Form):
    template_name = "feedback.html"
    email = forms.EmailField(required=False, validators=[is_cabinet_office_email])
    content = forms.TextInput()

