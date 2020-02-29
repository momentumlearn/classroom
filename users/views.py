from django.shortcuts import get_object_or_404, redirect, render
from .models import Team
# Create your views here.


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, "users/team_detail.html", {"team": team})
