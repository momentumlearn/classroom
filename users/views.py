from datetime import date

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeamInvitationForm
from .models import Team


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    previous_evaluations = team.scheduled_evaluations.filter(
        start_date__lt=date.today()).order_by('-start_date')
    return render(
        request, "users/team_detail.html", {
            "team": team,
            "members": team.members.all(),
            "previous_evaluations": previous_evaluations
        })


def team_invite(request, pk):
    team = get_object_or_404(Team, pk=pk)
    form = TeamInvitationForm(team=team)

    if request.method == "POST":
        form = TeamInvitationForm(team=team, data=request.POST)
        if form.is_valid():
            users = form.save()
            messages.success(request, f'{len(users)} users added to {team}.')
            return redirect(to='team_invite', pk=team.pk)

    return render(request, "users/team_invite.html", {
        "team": team,
        "form": form
    })
