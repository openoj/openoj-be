from rest_framework import permissions


class ProblemPermission(permissions.BasePermission):
    """
    只有拥有题目查看权限的用户可见，只有拥有题目修改权限的用户可以修改，只有拥有题目创建权限的用户可以创建
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('problem.can_view_problem')
        if request.method == 'POST':
            return request.user.has_perm('problem.can_add_problem')
        if request.method == 'PUT':
            return request.user.has_perm('problem.can_change_problem')
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('problem.can_view_problem')
        if request.method == 'POST':
            return request.user.has_perm('problem.can_add_problem')
        if request.method == 'PUT':
            return request.user.has_perm('problem.can_change_problem')
        return False
