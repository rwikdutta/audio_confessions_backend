from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import ConfessionsViewSet, OrderedConfessionsViewSet
from .views import AddConfessionView,ConfessionStudentFilterView

router=DefaultRouter()
router.register(r'confessions',ConfessionsViewSet)
router.register(r'orderedconfessions',OrderedConfessionsViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^addconfession/$',AddConfessionView.as_view()))
urlpatterns.append(url(r'^confessionstudentfilter/$',ConfessionStudentFilterView.as_view(),name='confessionstudentfilter'))