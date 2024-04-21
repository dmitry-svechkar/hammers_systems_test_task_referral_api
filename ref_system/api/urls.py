from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import RegistationViewSet, LoginUserView, ProfileViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


router = DefaultRouter()

router.register(
    'profile',
    ProfileViewSet,
    basename='profile',
)


urlpatterns = [
    path('', include(router.urls)),
    path('registation/',
         RegistationViewSet.as_view({'post': 'create'}),
         name='registation'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
