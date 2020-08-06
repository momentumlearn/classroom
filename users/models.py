from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from allauth.utils import build_absolute_uri
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

USER_TYPES = {
    "student": 1,
    "instructor": 2,
    "staff": 3,
}


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    USER_TYPE_CHOICES = (
        (USER_TYPES["student"], "Student"),
        (USER_TYPES["instructor"], "Instructor"),
        (USER_TYPES["staff"], "Staff"),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    team = models.ForeignKey(
        to=Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    def is_student(self):
        return is_student(self)

    def is_instructor(self):
        return is_instructor(self)

    def is_staff(self):
        return is_staff(self)

    def scheduled_evaluations(self):
        if not self.is_student():
            return []

        return self.team.scheduled_evaluations.exclude(
            pk__in=[e.scheduled_by.pk for e in self.evaluations.all()]
        )

    def send_new_account_reset_password_email(self, request=None):
        """
        When we create a new account for a user, we need to send them an email
        so they can reset their password.
        """
        token_generator = EmailAwarePasswordResetTokenGenerator()
        temp_key = token_generator.make_token(self)
        path = reverse(
            "account_reset_password_from_key",
            kwargs=dict(uidb36=user_pk_to_url_str(self), key=temp_key),
        )
        url = build_absolute_uri(request, path)
        current_site = get_current_site(request)
        context = {
            "current_site": current_site,
            "user": self,
            "password_reset_url": url,
        }
        message = render_to_string("users/reset_password_email.txt", context)
        send_mail(
            f"You have a new account at {current_site.name}",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
        )

    def __str__(self):
        return self.email


def is_student(user):
    return user.user_type == USER_TYPES["student"] and user.team is not None


def is_instructor(user):
    return user.user_type == USER_TYPES["instructor"]


def is_staff(user):
    return user.user_type == USER_TYPES["staff"]

