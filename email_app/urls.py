from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet, PeopleViewSet, PeopleExternalCCViewSet, PeopleExternalBCCViewSet, \
    PeopleInternalTOViewSet, PeopleInternalBCCViewSet, EmailContentViewSet, NotificationSettingsViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'people', PeopleViewSet)
router.register(r'people_external_cc', PeopleExternalCCViewSet)
router.register(r'people_external_bcc', PeopleExternalBCCViewSet)
router.register(r'people_internal_to', PeopleInternalTOViewSet)
router.register(r'people_internal_bcc', PeopleInternalBCCViewSet)
router.register(r'email_content', EmailContentViewSet)
router.register(r'notification_settings', NotificationSettingsViewSet, basename='notification_settings')

urlpatterns = [
    path('', include(router.urls)),
]
