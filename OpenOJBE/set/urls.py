from django.conf.urls import url

from set import views as set_views

urlpatterns = [
    url(r'^set_password$', set_views.CheckSetPermission.as_view()),
]
