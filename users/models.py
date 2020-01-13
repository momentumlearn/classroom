from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPES = {
    'student': 1,
    'instructor': 2,
    'staff': 3,
}


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    USER_TYPE_CHOICES = (
        (USER_TYPES['student'], 'Student'),
        (USER_TYPES['instructor'], 'Instructor'),
        (USER_TYPES['staff'], 'Staff'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,
                                                 default=1)
    team = models.ForeignKey(to=Team,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='members')

    def is_student(self):
        return is_student(self)

    def is_instructor(self):
        return is_instructor(self)

    def scheduled_evaluations(self):
        if not self.is_student():
            return []

        return self.team.scheduled_evaluations.exclude(
            pk__in=[e.scheduled_by.pk for e in self.evaluations.all()])

    def __str__(self):
        return self.email


def is_student(user):
    return user.user_type == USER_TYPES['student'] and user.team is not None


def is_instructor(user):
    return user.user_type == USER_TYPES['instructor']
