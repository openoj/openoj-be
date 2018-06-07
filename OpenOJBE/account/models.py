from django.contrib.auth.models import User
from django.db import models

email_code_subject = '[OpenOJ] Your Verification Code'
email_code_content = '''<p>Hello,<br/></p>
<p>Your verification code: <strong style="font-size: 150%%;">{code}</strong></p>
<p>Please use it within 24 hours.</p>
<p><br/></p>
<p>OpenOJ Team</p>
'''


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, db_index=True, unique=True)
    email = models.EmailField(max_length=128, db_index=True, unique=True)

    def __str__(self):
        return self.user.username


class EmailConfig(models.Model):
    email = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class EmailConfirm(models.Model):
    email = models.EmailField(max_length=128)
    code = models.CharField(max_length=128)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


def email_filter(email):
    """
    规范 email 的格式，清除掉其中的 + 和 .
    :param email:
    :return: 规范后的 email

    >>> email_filter('MeiK2333@gmail.com')
    meik2333@gmail.com
    >>> email_filter('meik2333@gmail.com')
    meik2333@gmail.com
    >>> email_filter('meik2333+title@gmail.com')
    meik2333@gmail.com
    >>> email_filter('m.e.i.k.2333+title@gmail.com')
    meik2333@gmail.com
    """
    email = email.lower()
    if '+' in email:
        email = '@'.join([email.split('+')[0], email.split('@')[-1]])
    if '.' in email.split('@')[0]:
        email = '@'.join([''.join(email.split('@')[0].split('.')), email.split('@')[-1]])
    return email


def username_filter(username):
    """
    规范 username 的格式
    :param username:
    :return:

    >>> username_filter('MeiK')
    meik
    """
    username = username.lower()
    return username


def check_email(email):
    """
    验证 email 是否可用
    :param email:
    :return: True or False
    """
    email = email_filter(email).split('@')[-1]
    return True if EmailConfig.objects.filter(email=email) else False
