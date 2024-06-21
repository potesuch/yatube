from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView,
                                   SpectacularRedocView)

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

app_name = 'api'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='api:schema'),
         name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'),
         name='redoc')
]
