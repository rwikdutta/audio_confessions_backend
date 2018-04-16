from .views import CommentView, CommentFilterView,AddCommentView
from django.conf.urls import url
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register(r'comment',CommentView)
urlpatterns=router.urls
urlpatterns.append(url(r'^commentfilter/$',CommentFilterView.as_view(),name='commentfilter'))
urlpatterns.append(url(r'^addcomment/$',AddCommentView.as_view()))