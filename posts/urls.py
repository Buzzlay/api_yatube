from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from posts import views

post_router = DefaultRouter()
comment_router = DefaultRouter()

post_router.register(
    'api/v1/posts',
    views.PostViewSet,
)
comment_router.register(
    r'api/v1/posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/api-token-auth/', obtain_auth_token),
]

urlpatterns += post_router.urls
urlpatterns += comment_router.urls
