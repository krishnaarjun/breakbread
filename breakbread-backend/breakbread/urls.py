from django.urls import include, path
from django.conf.urls import url
from authentication import routes as user_routes
from potluck import routes as potluck_routes
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^api/', include(user_routes)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api/potluck/', include(potluck_routes)),
]
