from django.shortcuts import get_object_or_404, redirect, render
from .models import Team
from .forms import TeamInvitationForm
from django.contrib import messages


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, "users/team_detail.html", {"team": team})


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
