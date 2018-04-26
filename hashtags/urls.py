from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import TagViewSet,OrderedTagViewSet,TagConfessionFilterView,TagAskFilterView

router=DefaultRouter()
router.register(r'tags',TagViewSet)
router.register(r'orderedtags',OrderedTagViewSet)
urlpatterns=router.urls
urlpatterns.append(url(r'^tagconfessionfilter',TagConfessionFilterView.as_view(),name='tagconfessionfilter'))
urlpatterns.append(url(r'^tagaskfilter',TagAskFilterView.as_view(),name='tagaskfilter'))
