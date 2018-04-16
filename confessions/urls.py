from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import ConfessionsViewSet
from .views import AddConfessionView

router=DefaultRouter()
router.register(r'confessions',ConfessionsViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^addconfession/$',AddConfessionView.as_view()))