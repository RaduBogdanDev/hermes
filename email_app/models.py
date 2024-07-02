from django.db import models
from .validators import validate_birthday
from django.core.exceptions import ValidationError


class Language(models.Model):
    language = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.language


class People(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    birthday = models.CharField(max_length=5, validators=[validate_birthday])  # Format: dd/mm
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PeopleExternalCC(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class PeopleExternalBCC(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class PeopleInternalTO(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class PeopleInternalBCC(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class EmailContent(models.Model):
    language = models.OneToOneField(Language, on_delete=models.CASCADE, unique=True)
    email_external_content = models.TextField()
    email_external_subject = models.CharField(max_length=255)
    email_internal_content = models.TextField()
    email_internal_subject = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class NotificationSettings(models.Model):
    internal_time_notification = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.internal_time_notification} days before birthday"

    def clean(self):
        if NotificationSettings.objects.exists() and not self.pk:
            raise ValidationError('There can be only one NotificationSettings instance.')

    def save(self, *args, **kwargs):
        if not self.pk and NotificationSettings.objects.exists():
            raise ValidationError('There can be only one NotificationSettings instance.')
        return super(NotificationSettings, self).save(*args, **kwargs)
