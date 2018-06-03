from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.middleware.csrf import get_token


class UserLoginAPI(APIView):
    def post(self, request):
        """
        User login api
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            auth_logout(request)
        data = request.data
        user = authenticate(username=data.get("username"), password=data.get("password"))
        # None is returned if username or password is wrong
        if user:
            if not user.is_active:
                return Response({"state": "error", "msg": "Your account has been disabled"})
            auth_login(request, user)
            return Response({
                "csrfmiddlewaretoken": get_token(request),
                "state": "success"
            })
        else:
            return Response({"state": "error", "msg": "Invalid username or password"})


class UserLogoutAPI(APIView):
    def post(self, request):
        """
        User logout api
        :param request:
        :return:
        """
        auth_logout(request)
        return Response({
            "state": "success"
        })
