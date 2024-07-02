from django.contrib import admin
from django.forms import ModelForm, ValidationError
from .models import (
    Language, People, PeopleExternalCC, PeopleExternalBCC,
    PeopleInternalTO, PeopleInternalBCC, EmailContent, NotificationSettings
)


class PeopleForm(ModelForm):
    class Meta:
        model = People
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if People.objects.filter(email=email).exists():
            raise ValidationError("A person with this email already exists.")
        return email


class PeopleExternalCCForm(ModelForm):
    class Meta:
        model = PeopleExternalCC
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PeopleExternalCC.objects.filter(email=email).exists():
            raise ValidationError("A CC person with this email already exists.")
        return email


class PeopleExternalBCCForm(ModelForm):
    class Meta:
        model = PeopleExternalBCC
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PeopleExternalBCC.objects.filter(email=email).exists():
            raise ValidationError("A BCC person with this email already exists.")
        return email


class PeopleInternalTOForm(ModelForm):
    class Meta:
        model = PeopleInternalTO
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PeopleInternalTO.objects.filter(email=email).exists():
            raise ValidationError("An internal TO person with this email already exists.")
        return email


class PeopleInternalBCCForm(ModelForm):
    class Meta:
        model = PeopleInternalBCC
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PeopleInternalBCC.objects.filter(email=email).exists():
            raise ValidationError("An internal BCC person with this email already exists.")
        return email


class EmailContentForm(ModelForm):
    class Meta:
        model = EmailContent
        fields = '__all__'

    def clean_language(self):
        language = self.cleaned_data.get('language')
        if EmailContent.objects.filter(language=language).exists():
            raise ValidationError("Email content for this language already exists.")
        return language


class PeopleAdmin(admin.ModelAdmin):
    form = PeopleForm
    list_display = ('name', 'email', 'language', 'birthday', 'created_date', 'updated_date')
    search_fields = ('name', 'email')
    list_filter = ('language',)


class EmailContentAdmin(admin.ModelAdmin):
    form = EmailContentForm
    list_display = ('language', 'email_external_subject', 'email_internal_subject', 'created_date', 'updated_date')
    search_fields = ('email_external_subject', 'email_internal_subject')
    list_filter = ('language',)


class PeopleExternalCCAdmin(admin.ModelAdmin):
    form = PeopleExternalCCForm
    list_display = ('name', 'email', 'created_date', 'updated_date')
    search_fields = ('name', 'email')


class PeopleExternalBCCAdmin(admin.ModelAdmin):
    form = PeopleExternalBCCForm
    list_display = ('name', 'email', 'created_date', 'updated_date')
    search_fields = ('name', 'email')


class PeopleInternalTOAdmin(admin.ModelAdmin):
    form = PeopleInternalTOForm
    list_display = ('name', 'email', 'created_date', 'updated_date')
    search_fields = ('name', 'email')


class PeopleInternalBCCAdmin(admin.ModelAdmin):
    form = PeopleInternalBCCForm
    list_display = ('name', 'email', 'created_date', 'updated_date')
    search_fields = ('name', 'email')


admin.site.register(Language)
admin.site.register(People, PeopleAdmin)
admin.site.register(PeopleExternalCC, PeopleExternalCCAdmin)
admin.site.register(PeopleExternalBCC, PeopleExternalBCCAdmin)
admin.site.register(PeopleInternalTO, PeopleInternalTOAdmin)
admin.site.register(PeopleInternalBCC, PeopleInternalBCCAdmin)
admin.site.register(EmailContent, EmailContentAdmin)
admin.site.register(NotificationSettings)
