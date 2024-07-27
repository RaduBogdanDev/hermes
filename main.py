import sqlite3
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import smtplib
import os
from dotenv import load_dotenv
from db_initializer import initialize_database

# Load environment variables from .env file
load_dotenv()

# Email settings from .env file
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DELEGATED_EMAIL = os.getenv('DELEGATED_EMAIL')
DELEGATED_NAME = os.getenv('DELEGATED_NAME')

# Database settings
DATABASE_NAME = 'hermes.db'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the database is set up before running the main logic
initialize_database()


def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)


def fetch_one(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result


def fetch_all(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result


def insert_log(email_type, recipient, cc, bcc, subject, body, status, error_message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO EmailLog (email_type, recipient, cc, bcc, subject, body, sent_at, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (email_type, recipient, cc, bcc, subject, body, datetime.now(), status, error_message))
    conn.commit()
    conn.close()


def send_email(to, subject, body, cc=None, bcc=None, email_type=None):
    if isinstance(to, str):
        to = [to]
    if cc is None:
        cc = []
    if bcc is None:
        bcc = []

    msg = MIMEMultipart()
    msg['From'] = formataddr((DELEGATED_NAME, DELEGATED_EMAIL))
    msg['To'] = ', '.join(to)
    msg['Subject'] = subject

    if cc:
        msg['Cc'] = ', '.join(cc)
    if bcc:
        msg['Bcc'] = ', '.join(bcc)

    msg.attach(MIMEText(body, 'html'))

    try:
        logger.info(f'Sending email to: {to}, cc: {cc}, bcc: {bcc}')
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(DELEGATED_EMAIL, to + cc + bcc, msg.as_string())
            log_status = 'success'
            error_message = None
            logger.info('Email sent successfully')
    except Exception as e:
        log_status = 'failure'
        error_message = str(e)
        logger.error(f'Failed to send email: {error_message}')

    # Create a log entry
    insert_log(email_type, ', '.join(to), ', '.join(cc), ', '.join(bcc), subject, body, log_status, error_message)
    logger.info('Email log entry created')


def replace_placeholders(content, person):
    return content.replace('{person_name}', person['name']).replace('{person_email}', person['email']).replace(
        '{person_birthday}', person['birthday'])


def send_birthday_email(person):
    logger.info(f'Sending birthday email to {person["name"]} ({person["email"]})')
    email_content = fetch_one('SELECT * FROM EmailContent WHERE language_id=?', (person['language_id'],))

    subject = replace_placeholders(email_content[3], person)
    body = replace_placeholders(email_content[2], person)

    external_cc = [p[0] for p in fetch_all('SELECT email FROM PeopleExternalCC')]
    external_bcc = [p[0] for p in fetch_all('SELECT email FROM PeopleExternalBCC')]

    send_email(person['email'], subject, body, cc=external_cc, bcc=external_bcc, email_type='birthday')


def send_internal_notification_email(person):
    logger.info(f'Sending internal notification email for {person["name"]} ({person["email"]})')
    email_content = fetch_one('SELECT * FROM EmailContent WHERE language_id=?', (person['language_id'],))

    subject = replace_placeholders(email_content[5], person)
    body = replace_placeholders(email_content[4], person)

    internal_to = [p[0] for p in fetch_all('SELECT email FROM PeopleInternalTO')]
    internal_bcc = [p[0] for p in fetch_all('SELECT email FROM PeopleInternalBCC')]

    send_email(internal_to, subject, body, cc=[person['email']], bcc=internal_bcc, email_type='internal_notification')


def main():
    logger.info('Starting the email sending process...')
    today = datetime.now().strftime('%d/%m')
    logger.info(f'Today is {today}')

    notification_setting = fetch_one('SELECT internal_time_notification FROM NotificationSettings LIMIT 1')
    if notification_setting:
        internal_notification_days = notification_setting[0]
    else:
        logger.error('Notification settings not found')
        return

    # Send birthday emails
    people_with_birthday_today = fetch_all('SELECT * FROM People WHERE birthday=?', (today,))
    logger.info(f'Found {len(people_with_birthday_today)} people with birthdays today')
    for person in people_with_birthday_today:
        send_birthday_email({
            'name': person[2],
            'email': person[1],
            'birthday': person[4],
            'language_id': person[3]
        })

    # Send internal notification emails
    people = fetch_all('SELECT * FROM People')
    for person in people:
        birthday_date = datetime.strptime(person[4], '%d/%m')
        notification_date = birthday_date - timedelta(days=internal_notification_days)
        logger.info(notification_date)
        if notification_date.strftime('%d/%m') == today:
            logger.info(f'Today is {today} and time to notification is {notification_date} - YEEEEEEEEEEEEES')
            send_internal_notification_email({
                'name': person[2],
                'email': person[1],
                'birthday': person[4],
                'language_id': person[3]
            })


if __name__ == '__main__':
    main()
