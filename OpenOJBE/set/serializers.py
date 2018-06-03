from rest_framework import serializers

from set.models import Set, SetProblem
from problem.serializers import ProblemSerializer


class SetProblemSerializer(serializers.ModelSerializer):
    """ SetProblem 列表序列化 """

    # 在列表中只显示基本信息
    class Meta:
        model = SetProblem
        fields = ('url', 'id', 'index', 'title', 'problem', 'st')


class SetProblemDetailSerializer(serializers.ModelSerializer):
    """ SetProblem Detail 序列化 """

    problem = ProblemSerializer(read_only=True)

    # 在 Detail 中，显示题目详情
    class Meta:
        model = SetProblem
        fields = ('url', 'id', 'index', 'title', 'problem', 'st')


class SetSerializer(serializers.ModelSerializer):
    """ Set 列表序列化 """

    user = serializers.CharField(default=serializers.CurrentUserDefault())
    password = serializers.CharField(write_only=True, allow_blank=True)

    # 列表中显示基本信息
    class Meta:
        model = Set
        fields = ('url', 'id', 'title', 'created_at', 'updated_at', 'started_at', 'ended_at', 'password', 'user')


class SetDetailSerializer(serializers.ModelSerializer):
    """ Set Detail 序列化 """

    user = serializers.CharField(default=serializers.CurrentUserDefault())
    set_problem = SetProblemSerializer(many=True, read_only=True)

    # Set Detail 中显示具体信息
    class Meta:
        model = Set
        fields = ('url', 'id', 'title', 'description', 'created_at', 'updated_at', 'started_at', 'ended_at',
                  'set_problem', 'user')
