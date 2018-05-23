from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=128)  # 题目标题
    content = models.TextField()  # 题目主体（ MarkDown 类型）
    source = models.CharField(max_length=128, blank=True)  # 题目来源
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 修改时间
    time_limit = models.IntegerField(default=1000)  # 时间限制
    memory_limit = models.IntegerField(default=32767)  # 内存限制
    length_limit = models.IntegerField(default=1024 * 1024)  # 提交代码长度限制

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'problem'
        permissions = (
            ("can_view_problem", "可以查看题目 / 可以将题目添加至 Set"),
        )
