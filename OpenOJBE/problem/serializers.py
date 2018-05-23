from rest_framework import serializers

from problem.models import Problem


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        fields = (
            'url', 'id', 'title', 'content', 'source', 'created_at', 'updated_at', 'time_limit', 'memory_limit',
            'length_limit')
