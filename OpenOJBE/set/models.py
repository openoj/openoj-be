from django.db import models
from django.contrib.auth.models import User

from problem.models import Problem


class Set(models.Model):
    title = models.CharField(max_length=128)  # Set 标题
    description = models.TextField(blank=True)  # Set 描述
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
    started_at = models.DateTimeField()  # 开始时间
    ended_at = models.DateTimeField()  # 结束时间
    password = models.CharField(max_length=128, blank=True)  # 密码（如果为空则为开放 Set ）

    def __str__(self):
        return self.title


class SetProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)  # 对应在题库中的题目
    st = models.ForeignKey(Set, on_delete=models.CASCADE)  # 对应的 Set
    index = models.IntegerField()  # 在 Set 中的顺序
    title = models.CharField(max_length=128)  # 在 Set 中的标题

    def __str__(self):
        return self.title


class SetUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 对应的用户
    st = models.ForeignKey(Set, on_delete=models.CASCADE)  # 对应的 Set
    password = models.CharField(max_length=128, blank=True)  # 激活密码（如果不为空，则每次登陆需要重新验证）

    def __str__(self):
        return self.user.username + ': ' + self.st.title
