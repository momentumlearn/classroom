from adminsortable.models import SortableMixin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from users.models import Team

User = get_user_model()


class Skill(SortableMixin):
    class Category(models.TextChoices):
        FRONT_END = 'fe', 'Front End'
        BACK_END = 'be', 'Back End'
        DEV_TOOLS = 'dt', 'Dev Tools'
        AGILE = 'ag', 'Agile Development'
        SOFT_SKILLS = 'ss', 'Soft Skills'
        GENERAL = 'ge', 'General'

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    levels = ArrayField(base_field=models.CharField(max_length=500), size=4)
    order = models.PositiveIntegerField(default=0,
                                        editable=False,
                                        db_index=True)
    version = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=2,
                                choices=Category.choices,
                                null=True,
                                blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ScheduledEvaluation(models.Model):
    team = models.ForeignKey(to=Team,
                             on_delete=models.PROTECT,
                             related_name="scheduled_evaluations")
    start_date = models.DateField()
    skills = models.ManyToManyField(to=Skill, related_name="+")


class Evaluation(models.Model):
    scheduled_by = models.ForeignKey(to=ScheduledEvaluation,
                                     related_name="evaluations",
                                     on_delete=models.PROTECT)
    user = models.ForeignKey(to=User,
                             related_name="evaluations",
                             on_delete=models.PROTECT)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.evaluated_at}"


class SkillEvaluation(models.Model):
    evaluation = models.ForeignKey(to=Evaluation,
                                   related_name="skill_evaluations",
                                   on_delete=models.CASCADE)
    skill = models.ForeignKey(to=Skill,
                              related_name="skill_evaluations",
                              on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(4)])
