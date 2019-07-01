from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .viewsets import PotluckSurveyViewset, HowYouHeardViewset, GroupsList, PotluckGroupViewSet, SurveyCSVViewset, PotluckFoodViewset, PotluckFoodGroupViewset, PotluckSelectFoodViewset

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'surveys', PotluckSurveyViewset)
router.register(r'heardfrom', HowYouHeardViewset)
router.register(r'foods', PotluckFoodViewset)
router.register(r'foodgroups', PotluckFoodGroupViewset)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^get_groups/', GroupsList.as_view(), name='GroupsList'),
    url(r'^survey_csv/', SurveyCSVViewset.as_view(), name="SurveyCSV"),
    url(r'^potluckgroup/(?P<potluck_id>[0-9a-fA-F-]+)?$',
        PotluckGroupViewSet.as_view(), name='ExistingGroups'),
    url(r'^select_food/group/(?P<group_id>[^/]+)/user/(?P<user_id>[^/]+)/$',
        PotluckSelectFoodViewset.as_view(), name='SelectFood')
]
