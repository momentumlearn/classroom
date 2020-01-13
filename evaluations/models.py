from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import ArrayField
from django_better_admin_arrayfield.models.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Team

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    levels = ArrayField(base_field=models.CharField(max_length=500), size=4)

    def __str__(self):
        return self.name


class ScheduledEvaluation(models.Model):
    team = models.ForeignKey(to=Team,
                             on_delete=models.PROTECT,
                             related_name="scheduled_evaluations")
    start_date = models.DateField()
    skills = models.ManyToManyField(to=Skill, related_name='+')


class Evaluation(models.Model):
    scheduled_by = models.ForeignKey(to=ScheduledEvaluation,
                                     on_delete=models.PROTECT)
    user = models.ForeignKey(to=User,
                             related_name='evaluations',
                             on_delete=models.PROTECT)
    evaluated_on = models.DateField(auto_now_add=True)


class SkillEvaluation(models.Model):
    evaluation = models.ForeignKey(to=Evaluation,
                                   related_name='skill_evaluations',
                                   on_delete=models.PROTECT)
    skill = models.ForeignKey(to=Skill,
                              related_name='skill_evaluations',
                              on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(4)])
