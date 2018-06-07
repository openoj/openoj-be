from rest_framework import serializers

from solution.models import Solution
from set.models import SetProblem


class SolutionProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetProblem
        fields = ('id', 'st', 'index')


class SolutionSerializer(serializers.ModelSerializer):
    """ Solution 列表序列化 """

    user = serializers.CharField(default=serializers.CurrentUserDefault())
    code = serializers.CharField(write_only=True)
    result = serializers.CharField(read_only=True)
    time_used = serializers.CharField(read_only=True)
    memory_used = serializers.CharField(read_only=True)
    submitted_at = serializers.DateTimeField(read_only=True)
    problem = SolutionProblemSerializer(read_only=True)

    # 在列表中只显示基本信息
    class Meta:
        model = Solution
        fields = (
            'url', 'id', 'user', 'problem', 'time_used', 'memory_used', 'result', 'language', 'code',
            'submitted_at')


class SolutionDetailSerializer(serializers.ModelSerializer):
    """ Solution 详情序列化 """

    class Meta:
        model = Solution
        fields = (
            'url', 'id', 'user', 'problem', 'time_used', 'memory_used', 'result', 'language',
            'submitted_at', 'info', 'code'
        )
