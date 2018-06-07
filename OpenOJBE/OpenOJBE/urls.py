"""OpenOJBE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include

from problem import views as problem_views
from set import views as set_views
from solution import views as solution_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'problem', problem_views.ProblemViewSet)
router.register(r'set', set_views.SetViewSet)
router.register(r'set_problem', set_views.SetProblemViewSet)
router.register(r'solution', solution_views.SolutionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('account.urls')),
    url(r'^', include('set.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
