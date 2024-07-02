from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Language, People, PeopleExternalCC, PeopleExternalBCC, PeopleInternalTO, PeopleInternalBCC, \
    EmailContent, NotificationSettings, EmailLog
from .serializers import LanguageSerializer, PeopleSerializer, PeopleExternalCCSerializer, PeopleExternalBCCSerializer, \
    PeopleInternalTOSerializer, PeopleInternalBCCSerializer, EmailContentSerializer, NotificationSettingsSerializer, \
    EmailLogSerializer


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


class NotificationSettingsViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer

    def get_object(self):
        # Ensure only one NotificationSettings object exists
        queryset = self.get_queryset()
        obj = queryset.first()
        if obj is None:
            # If no instance exists, create a default one
            obj = NotificationSettings.objects.create(internal_time_notification=0)
        return obj

    def retrieve(self, request, *args, **kwargs):
        # Override retrieve to get the single instance without needing an ID
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Override update to get the single instance without needing an ID
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
