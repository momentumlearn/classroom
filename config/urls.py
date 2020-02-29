"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from evaluations import views as evaluations_views
from users import views as users_views
from django.views.generic.base import RedirectView
from django.conf import settings


def trigger_error(request):
    raise RuntimeError("Triggered error")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('evaluations/', evaluations_views.evaluations, name='evaluations'),
    path('evaluations/<int:pk>/',
         evaluations_views.evaluation_student_detail,
         name='evaluation_detail'),
    path('evaluations/schedule/',
         evaluations_views.schedule_evaluation,
         name='schedule_evaluation'),
    path('evaluations/scheduled/<int:pk>/',
         evaluations_views.take_evaluation,
         name='take_evaluation'),
    path('evaluations/report/<int:pk>/',
         evaluations_views.evaluation_report,
         name='evaluation_report'),
    path('team/<int:pk>/', users_views.team_detail, name='team_detail'),
    path('team/<int:pk>/report/',
         evaluations_views.team_report,
         name='team_report'),
    path('team/<int:pk>/invite/', users_views.team_invite, name='team_invite'),
    path('health/', evaluations_views.health_check, name='health_check'),
    path('sentry-debug/', trigger_error),
    path('', RedirectView.as_view(url='/evaluations/'), name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
