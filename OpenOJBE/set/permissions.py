from rest_framework import permissions

from set.models import Set


class SetPermission(permissions.BasePermission):
    """
    Set 的权限控制
    """

    def has_permission(self, request, view):
        # 所有用户都可以请求 Set 的列表
        if request.method in permissions.SAFE_METHODS:
            return True
        # 拥有创建权限的用户才可以创建 Set
        if request.method == 'POST':
            return request.user.has_perm('problem.can_add_set')
        return False

    def has_object_permission(self, request, view, obj):
        # 只有拥有查看权限或者密码验证通过的用户可以查看
        if request.method in permissions.SAFE_METHODS or obj.passed(request):
            return request.user.has_perm('problem.can_view_set')
        # 拥有修改权限的用户才可以修改 Set
        if request.method == 'PUT':
            return request.user.has_perm('problem.can_change_set')
        return False


class SetProblemPermission(permissions.BasePermission):
    """
    SetProblem 的权限控制
    """

    def has_permission(self, request, view):
        if view.detail:
            return True
        # 不允许直接请求 SetProblem 的全部数据
        if request.method in permissions.SAFE_METHODS:
            if not request.GET.get('st'):
                return False
        return True

    def has_object_permission(self, request, view, obj):
        # 只有拥有查看权限或者密码验证通过的用户可以查看
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('problem.can_view_set')
        # 拥有修改权限的用户才可以修改 SetProblem
        if request.method == 'PUT':
            return request.user.has_perm('problem.can_change_set')
        return False
