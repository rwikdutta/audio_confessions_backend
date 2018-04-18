from .views import AskViewSet,AnswerAskView,AddAskView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url,include
router=DefaultRouter()
router.register(r'ask',AskViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^answerask/$',AnswerAskView.as_view()))
urlpatterns.append(url(r'^addask/$',AddAskView.as_view()))