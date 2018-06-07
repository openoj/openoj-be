from django.conf.urls import url

from account import views as account_views

urlpatterns = [
    url(r'^login$', account_views.UserLoginAPI.as_view()),
    url(r'^logout$', account_views.UserLogoutAPI.as_view()),
    url(r'^session$', account_views.SessionAPI.as_view()),
    url(r'^csrf$', account_views.CSRFTokenAPI.as_view()),
    url(r'^check_user', account_views.CheckRegisterAPI.as_view()),
    url(r'^register_email', account_views.RegisterEmailAPI.as_view()),
    url(r'^register', account_views.RegisterAPI.as_view())
]
