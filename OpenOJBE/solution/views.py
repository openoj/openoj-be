import django_filters
from rest_framework import viewsets
from rest_framework.views import APIView

from solution.models import Solution
from solution.permissions import SolutionPermission
from solution.serializers import SolutionDetailSerializer, SolutionSerializer


class SolutionFilter(django_filters.FilterSet):
    class Meta:
        model = Solution
        fields = {
            'id': ['exact', 'contains'],
            'user__username': ['exact', 'icontains'],
            'problem': ['exact'],
            'problem__index': ['exact'],
            'problem__st': ['exact'],
        }


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    filter_class = SolutionFilter
    permission_classes = (SolutionPermission,)

    def get_serializer_class(self):
        if self.detail:
            return SolutionDetailSerializer
        return SolutionSerializer
