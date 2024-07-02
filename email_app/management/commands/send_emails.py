# email_app/management/commands/send_emails.py

from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email_app.models import People, PeopleExternalCC, PeopleExternalBCC, PeopleInternalTO, PeopleInternalBCC, \
    EmailContent, NotificationSettings, EmailLog
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send birthday and internal notification emails'

    def handle(self, *args, **kwargs):
        logger.info('Starting the email sending process...')
        today = datetime.now().strftime('%d/%m')
        logger.info(f'Today is {today}')

        notification_setting = NotificationSettings.objects.first()
        if notification_setting:
            internal_notification_days = notification_setting.internal_time_notification
        else:
            self.stdout.write(self.style.ERROR('Notification settings not found'))
            logger.error('Notification settings not found')
            return

        # Send birthday emails
        people_with_birthday_today = People.objects.filter(birthday=today)
        logger.info(f'Found {len(people_with_birthday_today)} people with birthdays today')
        for person in people_with_birthday_today:
            self.send_birthday_email(person)

        # Send internal notification emails
        people = People.objects.all()
        for person in people:
            birthday_date = datetime.strptime(person.birthday, '%d/%m')
            notification_date = birthday_date - timedelta(days=internal_notification_days)
            if notification_date.strftime('%d/%m') == today:
                self.send_internal_notification_email(person)

    def send_birthday_email(self, person):
        logger.info(f'Sending birthday email to {person.name} ({person.email})')
        email_content = EmailContent.objects.get(language=person.language)

        subject = email_content.email_external_subject
        body = email_content.email_external_content

        external_cc = [p.email for p in PeopleExternalCC.objects.all()]
        external_bcc = [p.email for p in PeopleExternalBCC.objects.all()]

        self.send_email(person.email, subject, body, cc=external_cc, bcc=external_bcc, email_type='birthday')

    def send_internal_notification_email(self, person):
        logger.info(f'Sending internal notification email for {person.name} ({person.email})')
        email_content = EmailContent.objects.get(language=person.language)

        subject = email_content.email_internal_subject
        body = email_content.email_internal_content

        internal_to = [p.email for p in PeopleInternalTO.objects.all()]
        internal_bcc = [p.email for p in PeopleInternalBCC.objects.all()]

        self.send_email(internal_to, subject, body, cc=[person.email], bcc=internal_bcc,
                        email_type='internal_notification')

    def send_email(self, to, subject, body, cc=None, bcc=None, email_type=None):
        if isinstance(to, str):
            to = [to]
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []

        msg = MIMEMultipart()
        msg['From'] = settings.DELEGATED_EMAIL
        msg['To'] = ', '.join(to)
        msg['Subject'] = subject

        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        msg.attach(MIMEText(body, 'plain'))

        try:
            logger.info(f'Sending email to: {to}, cc: {cc}, bcc: {bcc}')
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.DELEGATED_EMAIL, to + cc + bcc, msg.as_string())
                log_status = 'success'
                error_message = None
                logger.info('Email sent successfully')
        except Exception as e:
            log_status = 'failure'
            error_message = str(e)
            logger.error(f'Failed to send email: {error_message}')

        # Create a log entry
        EmailLog.objects.create(
            email_type=email_type,
            recipient=', '.join(to),
            cc=', '.join(cc),
            bcc=', '.join(bcc),
            subject=subject,
            body=body,
            status=log_status,
            error_message=error_message
        )
        logger.info('Email log entry created')
