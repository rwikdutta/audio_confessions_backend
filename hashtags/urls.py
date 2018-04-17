from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import TagViewSet

router=DefaultRouter()
router.register(r'tags',TagViewSet)
urlpatterns=router.urls