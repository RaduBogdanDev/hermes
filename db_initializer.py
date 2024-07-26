import sqlite3
import os

DATABASE_NAME = 'hermes.db'


def database_exists():
    return os.path.isfile(DATABASE_NAME)


def get_existing_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]


def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Language (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS People (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        language_id INTEGER,
        birthday TEXT NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(language_id) REFERENCES Language(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PeopleExternalCC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PeopleExternalBCC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PeopleInternalTO (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PeopleInternalBCC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EmailContent (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language_id INTEGER,
        email_external_content TEXT NOT NULL,
        email_external_subject TEXT NOT NULL,
        email_internal_content TEXT NOT NULL,
        email_internal_subject TEXT NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(language_id),
        FOREIGN KEY(language_id) REFERENCES Language(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NotificationSettings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        internal_time_notification INTEGER NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK(id = 1)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EmailLog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_type TEXT NOT NULL,
        recipient TEXT NOT NULL,
        cc TEXT,
        bcc TEXT,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL,
        error_message TEXT
    )
    ''')


def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    existing_tables = get_existing_tables(cursor)

    expected_tables = [
        'Language', 'People', 'PeopleExternalCC', 'PeopleExternalBCC',
        'PeopleInternalTO', 'PeopleInternalBCC', 'EmailContent',
        'NotificationSettings', 'EmailLog'
    ]

    if set(existing_tables) != set(expected_tables):
        create_tables(cursor)
        conn.commit()
        print("Database created or updated successfully.")
    else:
        print("Database already up-to-date.")

    conn.close()


if __name__ == '__main__':
    initialize_database()
