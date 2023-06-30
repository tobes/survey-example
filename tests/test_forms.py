from django.core.exceptions import ValidationError
from django.test import TestCase, SimpleTestCase

from pulse_survey.survey import forms


# TODO - these tests should be changed if we add validation for Cabinet Office emails

class FeedbackFormTest(TestCase):
    def test_incorrect_email(self):
        form = forms.FeedbackForm({"email": "not an email", "content": ""})
        form.is_valid()
        email_errors = form.errors["email"]
        self.assertTrue("Enter a valid email address" in str(email_errors))

    def test_correct_email(self):
        form = forms.FeedbackForm({"email": "test@cabinetoffice.gov.uk", "content": "some feedback"})
        form.is_valid()
        no_email_errors = "email" not in form.errors
        self.assertTrue(no_email_errors)


class CabinetOfficeValidationTest(SimpleTestCase):
    def test_is_cabinet_office_email(self):
        valid_email = "valid@cabinetoffice.gov.uk"
        result = forms.is_cabinet_office_email(valid_email)
        self.assertTrue(result)

    def test_is_cabinet_office_email_invalid(self):
        valid_email = "invalid@not-cabinetoffice.gov.uk"
        with self.assertRaises(ValidationError):
            result = forms.is_cabinet_office_email(valid_email)


