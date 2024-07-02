from rest_framework import serializers
from .models import Language, People, PeopleExternalCC, PeopleExternalBCC, PeopleInternalTO, PeopleInternalBCC, \
    EmailContent, NotificationSettings, EmailLog


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PeopleSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = '__all__'

    def get_language(self, obj):
        return {
            'id': obj.language.id,
            'name': obj.language.language
        }


class PeopleExternalCCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleExternalCC
        fields = '__all__'


class PeopleExternalBCCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleExternalBCC
        fields = '__all__'


class PeopleInternalTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleInternalTO
        fields = '__all__'


class PeopleInternalBCCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleInternalBCC
        fields = '__all__'


class EmailContentSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = EmailContent
        fields = '__all__'

    def get_language(self, obj):
        return {
            'id': obj.language.id,
            'name': obj.language.language
        }


class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = '__all__'



class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'