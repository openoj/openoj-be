from rest_framework import serializers

from set.models import Set, SetProblem


class SetProblemSerializer(serializers.ModelSerializer):
    """ SetProblem 列表序列化 """

    # 在列表中只显示基本信息
    class Meta:
        model = SetProblem
        fields = ('url', 'id', 'index', 'title', 'problem', 'st')


class SetProblemDetailSerializer(serializers.ModelSerializer):
    """ SetProblem Detail 序列化 """

    content = serializers.CharField(source='problem.content')
    source = serializers.CharField(source='problem.source')
    created_at = serializers.CharField(source='problem.created_at')
    updated_at = serializers.CharField(source='problem.updated_at')
    time_limit = serializers.CharField(source='problem.time_limit')
    memory_limit = serializers.CharField(source='problem.memory_limit')
    length_limit = serializers.CharField(source='problem.length_limit')

    # 在 Detail 中，显示题目详情
    class Meta:
        model = SetProblem
        fields = ('url', 'id', 'index', 'title', 'problem', 'st', 'content', 'source', 'created_at', 'updated_at',
                  'time_limit', 'memory_limit', 'length_limit')


class SetSerializer(serializers.ModelSerializer):
    """ Set 列表序列化 """

    password = serializers.CharField(write_only=True)

    # 列表中显示基本信息
    class Meta:
        model = Set
        fields = ('url', 'id', 'title', 'created_at', 'updated_at', 'started_at', 'ended_at', 'password')


class SetDetailSerializer(serializers.ModelSerializer):
    """ Set Detail 序列化 """

    # Set Detail 中显示具体信息
    class Meta:
        model = Set
        fields = ('url', 'id', 'title', 'description', 'created_at', 'updated_at', 'started_at', 'ended_at',
                  'set_problem')
