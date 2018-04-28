from django.conf.urls import url
from .views import SignUp,SignIn,SignOut,CheckLogin,CheckAdminLogin,StudentViewSet,UpdateProfilePictureView,StudentUnpaginatedViewSet,ServerHealthTest
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'student',StudentViewSet)
router.register(r'studentfull',StudentUnpaginatedViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^signup/$',SignUp.as_view()))
urlpatterns.append(url(r'^signin/$', SignIn.as_view()))
urlpatterns.append(url(r'^signout/$', SignOut.as_view()))
urlpatterns.append(url(r'^checklogin/$', CheckLogin.as_view()))
urlpatterns.append(url(r'^checkadmin/$',CheckAdminLogin.as_view()))
urlpatterns.append(url(r'^updateprofilepicture/$',UpdateProfilePictureView.as_view()))
urlpatterns.append(url(r'^health/$',ServerHealthTest.as_view()))