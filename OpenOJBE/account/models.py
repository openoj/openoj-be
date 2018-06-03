from django.db import models


def email_filter(email):
    """
    规范 email 的格式，清除掉其中的 + 和 .
    :param email:
    :return: 规范后的 email

    >>> email_filter('meik2333@gmail.com')
    meik2333@gmail.com
    >>> email_filter('meik2333+title@gmail.com')
    meik2333@gmail.com
    >>> email_filter('m.e.i.k.2333+title@gmail.com')
    meik2333@gmail.com
    """
    if '+' in email:
        email = '@'.join([email.split('+')[0], email.split('@')[-1]])
    if '.' in email.split('@')[0]:
        email = '@'.join([''.join(email.split('@')[0].split('.')), email.split('@')[-1]])
    return email
