from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Evaluation, ScheduledEvaluation, SkillEvaluation


class BetterDateInput(forms.DateInput):
    input_type = 'date'


class ScheduledEvaluationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.form_action = 'schedule_evaluation'

        self.helper.add_input(
            Submit('submit',
                   'Schedule evaluation',
                   css_class="submit-button grow"))

    class Meta:
        model = ScheduledEvaluation
        fields = (
            'team',
            'start_date',
            'skills',
        )
        widgets = {
            'start_date': BetterDateInput,
            'skills': forms.CheckboxSelectMultiple
        }


class EvaluationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.scheduled_eval = kwargs.pop('scheduled_eval')
        super().__init__(*args, **kwargs)

        for skill in self.scheduled_eval.skills.all():
            self.fields[f'skill_{skill.pk}'] = forms.TypedChoiceField(
                label=skill.name,
                required=True,
                choices=[(i + 1, f"{i+1}. {level}")
                         for i, level in enumerate(skill.levels)],
                widget=forms.RadioSelect)

        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit('submit',
                   'Submit evaluation',
                   css_class="submit-button grow"))

    def save(self, user):
        if not self.is_valid():
            return False

        evaluation = Evaluation(scheduled_by=self.scheduled_eval, user=user)
        evaluation.save()

        for skill in self.scheduled_eval.skills.all():
            evaluation.skill_evaluations.create(
                skill=skill, score=self.cleaned_data[f'skill_{skill.pk}'])

        return evaluation
