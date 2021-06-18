from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Fieldset
from django import forms

from .models import Evaluation, ScheduledEvaluation, Skill


class BetterDateInput(forms.DateInput):
    input_type = "date"


class ScheduledEvaluationForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.filter(version=2))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_action = "schedule_evaluation"
        self.helper.layout = Layout(
            "team",
            "start_date",
            HTML(
                '<button type="button" id="check-all" class="f6 link ph3 pv2 mb2 dib white b btn--select-all">Check All</button>'
            ),
            "skills",
        )
        self.helper.add_input(
            Submit("submit",
                   "Schedule evaluation",
                   css_class="submit-button grow mt2"))

    class Meta:
        model = ScheduledEvaluation
        fields = (
            "team",
            "start_date",
            "skills",
        )
        widgets = {
            "start_date": BetterDateInput,
            "skills": forms.CheckboxSelectMultiple,
        }


class EvaluationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.scheduled_eval = kwargs.pop("scheduled_eval")
        super().__init__(*args, **kwargs)

        for skill in self.scheduled_eval.skills.all():
            self.fields[f"skill_{skill.pk}"] = forms.TypedChoiceField(
                label=skill.name,
                required=True,
                choices=([(i, f"{i}. {level}")
                          for i, level in enumerate(skill.levels)]),
                widget=forms.RadioSelect,
            )

        self.helper = FormHelper()

        self.helper.form_method = "post"

        self.helper.add_input(
            Submit("submit",
                   "Submit evaluation",
                   css_class="submit-button grow"))

    def save(self, user):
        if not self.is_valid():
            return False

        evaluation = Evaluation(scheduled_by=self.scheduled_eval, user=user)
        evaluation.save()

        for skill in self.scheduled_eval.skills.all():
            evaluation.skill_evaluations.create(
                skill=skill, score=self.cleaned_data[f"skill_{skill.pk}"])

        return evaluation
