from django.conf.urls import url
from .views import SignUp,SignIn,SignOut,CheckLogin,CheckAdminLogin

urlpatterns=[
    url(r'^signup/$',SignUp.as_view()),
    url(r'^signin/$', SignIn.as_view()),
    url(r'^signout/$', SignOut.as_view()),
    url(r'^checklogin/$', CheckLogin.as_view()),
    url(r'^checkadmin/$',CheckAdminLogin.as_view()),
]