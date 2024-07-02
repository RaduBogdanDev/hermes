from rest_framework import viewsets
from .models import Language, People, PeopleExternalCC, PeopleExternalBCC, PeopleInternalTO, PeopleInternalBCC, \
    EmailContent, NotificationSettings
from .serializers import LanguageSerializer, PeopleSerializer, PeopleExternalCCSerializer, PeopleExternalBCCSerializer, \
    PeopleInternalTOSerializer, PeopleInternalBCCSerializer, EmailContentSerializer, NotificationSettingsSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class PeopleViewSet(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer


class PeopleExternalCCViewSet(viewsets.ModelViewSet):
    queryset = PeopleExternalCC.objects.all()
    serializer_class = PeopleExternalCCSerializer


class PeopleExternalBCCViewSet(viewsets.ModelViewSet):
    queryset = PeopleExternalBCC.objects.all()
    serializer_class = PeopleExternalBCCSerializer


class PeopleInternalTOViewSet(viewsets.ModelViewSet):
    queryset = PeopleInternalTO.objects.all()
    serializer_class = PeopleInternalTOSerializer


class PeopleInternalBCCViewSet(viewsets.ModelViewSet):
    queryset = PeopleInternalBCC.objects.all()
    serializer_class = PeopleInternalBCCSerializer


class EmailContentViewSet(viewsets.ModelViewSet):
    queryset = EmailContent.objects.all()
    serializer_class = EmailContentSerializer


class NotificationSettingsViewSet(viewsets.ModelViewSet):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
