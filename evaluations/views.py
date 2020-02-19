from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import is_student, is_instructor
from datetime import date
from .models import ScheduledEvaluation
from .forms import ScheduledEvaluationForm, EvaluationForm
from django.urls import reverse


@login_required
@user_passes_test(lambda u: is_student(u) or is_instructor(u))
def evaluations(request):
    if request.user.is_student():
        return evaluations_student(request)
    return evaluations_instructor(request)


def evaluations_student(request):
    return render(request, "evaluations/evaluations_student.html")


def evaluations_instructor(request):
    scheduled_evaluations = ScheduledEvaluation.objects.filter(
        start_date__gte=date.today()).order_by('start_date')
    return render(request, "evaluations/evaluations_instructor.html",
                  {"scheduled_evaluations": scheduled_evaluations})


@login_required
@user_passes_test(is_instructor)
def schedule_evaluation(request):
    if request.method == "POST":
        form = ScheduledEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="schedule_evaluation")
    else:
        form = ScheduledEvaluationForm()

    return render(request, "evaluations/schedule.html", {"form": form})


@login_required
@user_passes_test(is_student)
def take_evaluation(request, pk):
    scheduled_eval = get_object_or_404(request.user.team.scheduled_evaluations,
                                       pk=pk)

    if request.method == "POST":
        form = EvaluationForm(scheduled_eval=scheduled_eval, data=request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(to='evaluations')
    else:
        form = EvaluationForm(scheduled_eval=scheduled_eval)

    form.helper.form_action = reverse('take_evaluation', kwargs={'pk': pk})
    return render(request, "evaluations/take_evaluation.html", {"form": form})
