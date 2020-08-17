import re
import uuid

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import EmailValidator

from .models import User


def random_suffix():
    return str(uuid.uuid4())[:4]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class TeamInvitationForm(forms.Form):
    email_addresses = forms.CharField(
        widget=forms.Textarea,
        help_text="Separate email addresses by spaces, commas, or newlines.")

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team')

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit('submit', 'Invite to team', css_class="submit-button grow"))

    def clean_email_addresses(self):
        email_addresses = [
            e.strip() for e in re.split(r"\s*,\s*|\s+",
                                        self.cleaned_data['email_addresses'])
        ]
        for email in email_addresses:
            EmailValidator(
                message=f"{email} is not a valid email address.")(email)
        return email_addresses

    def save(self):
        print(self.cleaned_data['email_addresses'])

        users = []
        # TODO create users/add to team
        for email in self.cleaned_data['email_addresses']:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email.split('@')[0] + random_suffix()})
            if created:
                user.set_unusable_password()
                user.send_new_account_reset_password_email()
            user.team = self.team
            user.save()
            users.append(user)

        return users
