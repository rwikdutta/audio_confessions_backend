from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import LikesViewSet,LikesFilterView,AddLikesView

router=DefaultRouter()
router.register(r'likes',LikesViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^likesfilter/$',LikesFilterView.as_view(),name='likesfilter'))
urlpatterns.append(url(r'^addlikes/$',AddLikesView.as_view()))