from .views import AskViewSet,AnswerAskView,AddAskView,FromStudentAskFilterView,ToStudentAskFilterView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url,include
router=DefaultRouter()
router.register(r'ask',AskViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^answerask/$',AnswerAskView.as_view()))
urlpatterns.append(url(r'^addask/$',AddAskView.as_view()))
urlpatterns.append(url(r'^fromstudentfilter/$',FromStudentAskFilterView.as_view(),name='fromstudentfilter'))
urlpatterns.append(url(r'^tostudentfilter/$',ToStudentAskFilterView.as_view(),name='tostudentfilter'))
