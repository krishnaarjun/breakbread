from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewset, Signup

router = DefaultRouter()
router.register(r'users', UserViewset)
urlpatterns = [
    path('', include(router.urls)),
    path('signup/', Signup.as_view(), name='Signup')
]
