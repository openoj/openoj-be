from django.contrib import admin

from account.models import EmailConfig, UserProfile, EmailConfirm

admin.site.register(UserProfile)
admin.site.register(EmailConfig)
admin.site.register(EmailConfirm)
