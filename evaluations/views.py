from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from users.models import Team, is_instructor, is_student

from .forms import EvaluationForm, ScheduledEvaluationForm
from .models import Evaluation, ScheduledEvaluation, Skill

User = get_user_model()


def health_check(request):
    return render(request, "evaluations/health_check.html")


@login_required
@user_passes_test(lambda u: u.is_instructor() or u.is_staff())
@login_required
def evaluations(request):
    """
    For students, show a list of their upcoming evaluations and previous evaluations.
    For instructors, show them all upcoming and previous evaluations.
    """

    def evaluations_student():
        evaluations = request.user.evaluations.order_by("evaluated_at").annotate(
            avg_score=Avg("skill_evaluations__score")
        )
        last_evaluation = request.user.evaluations.order_by("-evaluated_at").first()
        if last_evaluation:
            skill_evaluations = last_evaluation.skill_evaluations.order_by(
                "skill__name"
            )
        else:
            skill_evaluations = []
        return render(
            request,
            "evaluations/evaluations_student.html",
            {
                "evaluations": evaluations,
                "js_data": {
                    "skills_labels": [e.skill.name for e in skill_evaluations],
                    "skills_scores": [e.score for e in skill_evaluations],
                    "evaluation_dates": [
                        e.evaluated_at.strftime("%Y-%m-%d") for e in evaluations
                    ],
                    "evaluation_avgs": [e.avg_score for e in evaluations],
                },
            },
        )

    def evaluations_instructor():
        scheduled_evaluations = ScheduledEvaluation.objects.filter(
            start_date__gte=date.today()
        ).order_by("start_date")
        previous_evaluations = ScheduledEvaluation.objects.filter(
            start_date__lt=date.today()
        ).order_by("-start_date")
        return render(
            request,
            "evaluations/evaluations_instructor.html",
            {
                "scheduled_evaluations": scheduled_evaluations,
                "previous_evaluations": previous_evaluations,
            },
        )

    if request.user.is_instructor() or request.user.is_staff():
        return evaluations_instructor()
    return evaluations_student()


@login_required
@user_passes_test(lambda u: is_student(u) or is_instructor(u))
def evaluation_detail(request, pk):
    if is_instructor(request.user):
        evaluation = get_object_or_404(Evaluation, pk=pk)
    else:
        evaluation = get_object_or_404(request.user.evaluations, pk=pk)
    skill_evaluations = evaluation.skill_evaluations.order_by("skill__name")
    return render(
        request,
        "evaluations/evaluation_detail.html",
        {
            "evaluation": evaluation,
            "js_data": {
                "skills_labels": [e.skill.name for e in skill_evaluations],
                "skills_scores": [e.score for e in skill_evaluations],
            },
        },
    )


@login_required
@user_passes_test(is_student)
def evaluations_report(request):
    evaluations = request.user.evaluations.order_by("evaluated_at")
    all_skills_evaluated = Skill.objects.filter(
        skill_evaluations__evaluation__user=request.user
    ).distinct()

    report = {"dates": [], "skills": {s.name: None for s in all_skills_evaluated}}

    print([s.name for s in all_skills_evaluated])

    for evaluation in evaluations:
        report["dates"].append(evaluation.evaluated_at)
        for skill in all_skills_evaluated:
            skill_eval = evaluation.skill_evaluations.filter(skill=skill).first()
            if report["skills"][skill.name] is None:
                report["skills"][skill.name] = []
            if skill_eval:
                report["skills"][skill.name].append(skill_eval.score)
            else:
                report["skills"][skill.name].append("-")

    print(report)

    return render(request, "evaluations/evaluations_report.html", {"report": report})


@login_required
@user_passes_test(is_instructor)
def evaluation_report(request, pk):
    scheduled_evaluation = get_object_or_404(
        ScheduledEvaluation.objects.filter(start_date__lt=date.today()), pk=pk
    )

    skills = scheduled_evaluation.skills.annotate(
        count=Count(
            "skill_evaluations__score",
            filter=Q(skill_evaluations__evaluation__scheduled_by=scheduled_evaluation),
        ),
        avg=Avg(
            "skill_evaluations__score",
            filter=Q(skill_evaluations__evaluation__scheduled_by=scheduled_evaluation),
        ),
    )

    return render(
        request,
        "evaluations/evaluation_report.html",
        {
            "scheduled_evaluation": scheduled_evaluation,
            "skills": skills,
            "js_data": {
                "skills_labels": [s.name for s in skills],
                "skills_scores": [round(s.avg, 2) if s.avg else None for s in skills],
            },
        },
    )


@login_required
@user_passes_test(is_instructor)
def team_report(request, pk):
    team = get_object_or_404(Team, pk=pk)
    skills = Skill.objects.filter(
        skill_evaluations__evaluation__user__team=team
    ).annotate(count=Count("skill_evaluations"), avg=Avg("skill_evaluations__score"))

    evaluation_by_date = (
        Evaluation.objects.filter(scheduled_by__team=team)
        .annotate(date=F("scheduled_by__start_date"))
        .order_by("date")
        .values("date")
        .annotate(avg=Avg("skill_evaluations__score"))
    )

    return render(
        request,
        "evaluations/team_report.html",
        {
            "team": team,
            "skills": skills,
            "js_data": {
                "skills_labels": [s.name for s in skills],
                "skills_scores": [round(s.avg, 2) if s.avg else None for s in skills],
                "evaluations": list(evaluation_by_date),
            },
        },
    )


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
    scheduled_eval = get_object_or_404(request.user.team.scheduled_evaluations, pk=pk)

    if request.method == "POST":
        form = EvaluationForm(scheduled_eval=scheduled_eval, data=request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(to="evaluations")
    else:
        form = EvaluationForm(scheduled_eval=scheduled_eval)

    form.helper.form_action = reverse("take_evaluation", kwargs={"pk": pk})
    return render(request, "evaluations/take_evaluation.html", {"form": form})


@login_required
@user_passes_test(is_instructor)
def student_detail(request, pk):
    student = get_object_or_404(User, pk=pk)
    evaluations = student.evaluations.order_by("evaluated_at").annotate(
        avg_score=Avg("skill_evaluations__score")
    )
    last_evaluation = student.evaluations.order_by("-evaluated_at").first()
    if last_evaluation:
        skill_evaluations = last_evaluation.skill_evaluations.order_by("skill__name")
    else:
        skill_evaluations = []
    return render(
        request,
        "evaluations/student_detail.html",
        {
            "student": student,
            "evaluations": evaluations,
            "js_data": {
                "skills_labels": [e.skill.name for e in skill_evaluations],
                "skills_scores": [e.score for e in skill_evaluations],
                "evaluation_dates": [
                    e.evaluated_at.strftime("%Y-%m-%d") for e in evaluations
                ],
                "evaluation_avgs": [e.avg_score for e in evaluations],
            },
        },
    )
