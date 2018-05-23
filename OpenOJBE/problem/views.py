from rest_framework import viewsets

import django_filters

from problem.models import Problem
from problem.serializers import ProblemSerializer
from problem.permissions import ProblemPermission


class ProblemFilter(django_filters.FilterSet):
    class Meta:
        model = Problem
        fields = {
            'id': ['icontains'],
            'title': ['icontains'],
            'source': ['icontains'],
        }


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_class = ProblemFilter
    permission_classes = (ProblemPermission,)
