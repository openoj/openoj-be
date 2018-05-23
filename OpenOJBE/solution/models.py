from django.db import models
from django.contrib.auth.models import User

from set.models import SetProblem


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 提交用户
    problem = models.ForeignKey(SetProblem, on_delete=models.CASCADE)  # 提交题目
    time_used = models.IntegerField(default=0)  # 时间用量
    memory_used = models.IntegerField(default=0)  # 内存用量
    language = models.IntegerField()  # 提交语言
    result = models.IntegerField(default=0)  # 提交结果
    submitted_at = models.DateTimeField(auto_now_add=True)  # 提交时间
    code = models.TextField(max_length=1024 * 1024)  # 提交代码
    ip = models.CharField(max_length=128)  # 提交 IP
    info = models.TextField(max_length=1024 * 1024)  # Info 信息

    class Meta:
        db_table = 'solution'
