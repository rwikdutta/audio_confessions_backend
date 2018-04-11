from .views import CommentView
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'comment',CommentView)
urlpatterns=router.urls