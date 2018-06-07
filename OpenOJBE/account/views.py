import datetime
from random import randint

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import (EmailConfirm, User, UserProfile, check_email,
                            email_code_content, email_code_subject,
                            email_filter, username_filter)
from account.send_mail import AliyunMailSender


class SessionAPI(APIView):
    def get(self, request):
        """
        Get User Session
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            return Response({
                "logged_in": True,
                "user": {
                    "email": request.user.email,
                    "username": request.user.username
                }
            })
        return Response({
            "logged_in": False
        })


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
        username = data.get('login_name')
        password = data.get('password')
        user = UserProfile.objects.filter(username=username_filter(username))
        if not user:  # 如果 username 没有匹配，则去查看 email 有无匹配
            user_profile = UserProfile.objects.filter(email=email_filter(username))
            if user_profile:
                user = user_profile[0].user
        else:
            user = user[0].user
        # 若没有找到用户名或者密码错误
        if not user or not user.check_password(password):
            return Response({"result": "error", "msg": "Invalid username or password"})
        if user:
            if not user.is_active:
                return Response({"result": "error", "msg": "Your account has been disabled"})
            auth_login(request, user)
            return Response({
                "result": "success",
                "msg": "Welcome back, {}".format(user.username)
            })
        else:
            return Response({"result": "error", "msg": "Invalid username or password"})


class UserLogoutAPI(APIView):
    def get(self, request):
        """
        User logout api
        :param request:
        :return:
        """
        auth_logout(request)
        return Response({
            "result": "success",
            "msg": "You have logged out"
        })


class RegisterEmailAPI(APIView):
    def post(self, request):
        email = email_filter(request.data.get('email'))
        if UserProfile.objects.filter(email=email):
            return Response({
                "result": "error",
                "errors": {
                    "email": "The email has already been used"
                }
            })
        if check_email(email) is False:
            return Response({
                "result": "error",
                "errors": {
                    "email": "Unsupported email"
                }
            })
        res = EmailConfirm.objects.filter(email=email)
        if not res:
            res = EmailConfirm()
            res.email = email
            res.save()
        else:
            res = res[0]
            if (datetime.datetime.utcnow() - res.updated_at.replace(tzinfo=None)).total_seconds() < 60:
                return Response({
                    "result": "error",
                    "msg": "Take it easy and have a cup of java",
                    "retry_after": 60 - (datetime.datetime.utcnow() - res.updated_at.replace(tzinfo=None)).total_seconds()
                })
        res.code = str(randint(100000, 999999))
        res.save()

        aliyun_mail_sender = AliyunMailSender(settings.MAIL_ACCESS_KEY, settings.MAIL_ACCESS_SECRET)
        aliyun_mail_sender.single_send_mail(settings.MAIL_ACCOUNT, 'OpenOJ', res.email, email_code_subject,
                                            email_code_content.format(code=res.code))

        return Response({
            "result": "success",
            "msg": "The code has sent to your email",
            "retry_after": 60
        })


class RegisterAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('verification_code')
        email = email_filter(request.data.get('email'))
        password = request.data.get('password')

        if UserProfile.objects.filter(username=username_filter(username)):
            return Response({
                "result": "error",
                "errors": {
                    "username": "Username already exists"
                }
            })

        if UserProfile.objects.filter(email=email):
            return Response({
                "result": "error",
                "errors": {
                    "email": "Email already exists"
                }
            })

        res = EmailConfirm.objects.filter(email=email)
        if not res:
            return Response({
                "result": "error",
                "errors": {
                    "email": "Email does not exist"
                }
            })
        res = res[0]
        if res.code != code:
            return Response({
                "result": "error",
                "errors": {
                    "verification_code": "Wrong verification code"
                }
            })
        if (datetime.datetime.utcnow() - res.updated_at.replace(tzinfo=None)).total_seconds() > 24 * 60 * 60:
            return Response({
                "result": "error",
                "errors": {
                    "verification_code": "Verification code expired"
                }
            })

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        user_profile = UserProfile()
        user_profile.username = username_filter(username)
        user_profile.email = email
        user_profile.user = user
        user_profile.save()

        auth_login(request, user)

        return Response({
            "result": "success",
            "msg": "Welcome {}".format(user.username)
        })


class CheckRegisterAPI(APIView):
    def get(self, request):
        data = request.GET
        result = {
            "result": "success",
            "username": False,
            "email": False
        }
        if data.get("username"):
            result["username"] = UserProfile.objects.filter(username=username_filter(data.get("username"))).exists()
        if data.get("email"):
            result["email"] = UserProfile.objects.filter(email=email_filter(data.get("email"))).exists()
        if check_email(data.get('email')) is False:
            result['result'] = 'error'
            result['msg'] = 'unsupported email'
        else:
            result['result'] = 'error'
        return Response(result)


class CSRFTokenAPI(APIView):
    def get(self, request):
        return Response({
            "result": "success",
            "csrfmiddlewaretoken": get_token(request)
        })
