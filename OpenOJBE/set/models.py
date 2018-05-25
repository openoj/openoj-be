from django.db import models
from django.contrib.auth.models import User

from problem.models import Problem


class Set(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 创建者
    title = models.CharField(max_length=128)  # Set 标题
    description = models.TextField(blank=True)  # Set 描述
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
    started_at = models.DateTimeField()  # 开始时间
    ended_at = models.DateTimeField()  # 结束时间
    password = models.CharField(max_length=128, blank=True)  # 密码（如果为空则为开放 Set ）

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'set'
        permissions = (
            ("can_view_set", "可以绕过密码查看 Set"),
        )

    def passed(self, request):
        # 如果 Set 没有密码，则任何人可见
        if not self.password:
            return True
        # 如果拥有查看权限，则可见
        if request.user.has_perm('set.can_view_set'):
            return True
        # 如果是创建者，则可见
        if self.user == request.user:
            return True
        set_user = SetUser.objects.filter(st=self, user=request.user)
        # 如果没有登录成功过，则不可见
        if not set_user:
            return False
        set_user = set_user[0]
        # 如果 SetUser 没有密码保护，则可见
        if not set_user.password:
            return True
        # 如果有密码保护，则验证 IP 是否相同
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        # 若 IP 相同，则可见
        if set_user.ip == ip:
            return True
        # 否则需要重新验证授权
        return False


class SetProblem(models.Model):
    problem = models.ForeignKey(Problem, related_name='set_problem', on_delete=models.CASCADE)  # 对应在题库中的题目
    st = models.ForeignKey(Set, related_name='set_problem', on_delete=models.CASCADE)  # 对应的 Set
    index = models.IntegerField()  # 在 Set 中的顺序
    title = models.CharField(max_length=128)  # 在 Set 中的标题

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'set_problem'
        ordering = ['index']
        unique_together = ('st', 'index')  # 设置联合主键，保证同一个 Set 中的 index 不重复


class SetUser(models.Model):
    user = models.ForeignKey(User, related_name='set_user', on_delete=models.CASCADE)  # 对应的用户
    st = models.ForeignKey(Set, on_delete=models.CASCADE)  # 对应的 Set
    password = models.CharField(max_length=128, blank=True)  # 激活密码（如果不为空，则每次更换 IP 需要重新验证）
    ip = models.CharField(max_length=128, blank=True)  # 激活 IP

    class Meta:
        db_table = 'set_user'
