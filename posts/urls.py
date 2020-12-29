from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(
    r'posts',
    PostViewSet,
    basename='post'
)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', obtain_auth_token),
]
