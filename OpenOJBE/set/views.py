from rest_framework import viewsets

import django_filters

from set.models import Set, SetProblem
from set.serializers import SetSerializer, SetProblemSerializer, SetDetailSerializer, SetProblemDetailSerializer
from set.permissions import SetPermission, SetProblemPermission

from oauth2_provider.contrib.rest_framework import TokenHasScope


class SetFilter(django_filters.FilterSet):
    class Meta:
        model = Set
        fields = {
            'id': ['icontains'],
            'title': ['icontains'],
        }


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    filter_class = SetFilter
    permission_classes = (SetPermission, TokenHasScope)

    def get_serializer_class(self):
        if self.detail:
            return SetDetailSerializer
        return SetSerializer


class SetProblemFilter(django_filters.FilterSet):
    class Meta:
        model = SetProblem
        fields = {
            'st': ['exact'],
        }


class SetProblemViewSet(viewsets.ModelViewSet):
    queryset = SetProblem.objects.all()
    serializer_class = SetProblemSerializer
    filter_class = SetProblemFilter
    permission_classes = (SetProblemPermission, TokenHasScope)

    def get_serializer_class(self):
        if self.detail:
            return SetProblemDetailSerializer
        return SetProblemSerializer
