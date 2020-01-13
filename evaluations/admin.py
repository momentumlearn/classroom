from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Skill, SkillEvaluation, Evaluation, ScheduledEvaluation


class SkillAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillEvaluation)
admin.site.register(Evaluation)
admin.site.register(ScheduledEvaluation)
