from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import Evaluation, ScheduledEvaluation, Skill, SkillEvaluation


class SkillAdmin(SortableAdmin, DynamicArrayMixin):
    pass


admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillEvaluation)
admin.site.register(Evaluation)
admin.site.register(ScheduledEvaluation)
