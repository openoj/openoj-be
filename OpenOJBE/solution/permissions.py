# coding=utf-8
from rest_framework import permissions

from set.models import SetProblem


class SolutionPermission(permissions.BasePermission):
    """ Solution 的权限控制 """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # 如果拥有查看权限，则可以查看任何人的
            if request.user.has_perm('solution.can_view_solution'):
                return True
            # 如果请求的是自己的，则可以返回
            if request.GET.get('username') == request.user.username:
                return True
            # 不允许直接请求所有数据
            if not request.GET.get('st'):
                return False
            return False
        problem = request.POST.get('problem')
        set_problem = SetProblem.objects.get(id=int(problem))
        if set_problem.st.passed(request) or request.user.has_perm('solution.can_add_solution'):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # 只有拥有查看权限或者密码验证通过的用户可以查看
        if request.method in permissions.SAFE_METHODS:
            if obj.problem.st.passed(request):
                return True
            else:
                return request.user.has_perm('problem.can_view_set')
        # 拥有修改权限的用户才可以修改 Solution
        if request.method == 'PUT':
            return request.user.has_perm('problem.can_change_solution')
        return False
