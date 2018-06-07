import django_filters
from rest_framework import viewsets

from problem.models import Problem
from problem.permissions import ProblemPermission
from problem.serializers import ProblemSerializer


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
    required_scopes = ['read']
    permission_classes = (ProblemPermission,)
