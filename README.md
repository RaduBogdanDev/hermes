
# Hermes Notification System

## Description
The Hermes Notification System is a Python application designed to send birthday and internal notification emails to users. It uses SQLite for data storage and an SMTP server for sending emails.

## Features
- Sends birthday emails to users based on their stored birthday dates.
- Sends internal notification emails a specified number of days before a user's birthday.
- Logs email activities in the database.
- Supports multiple languages for email content.

## Requirements
- Python 3.6+
- `python-dotenv` for managing environment variables
- SQLite3 (comes pre-installed with Python)

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory with the following content:

    ```plaintext
    EMAIL_HOST= SMTP
    EMAIL_PORT= Email Port
    EMAIL_USE_TLS= True of ralse
    EMAIL_HOST_USER= Host email address
    EMAIL_HOST_PASSWORD=P Host email password
    DELEGATED_EMAIL= Delegated email permission
    DELEGATED_NAME= Name of the email address
    ```

## Database Initialization

Ensure that the database is set up by running the database initialization script. This step is automatically handled when running the main script.

## Usage

Run the main script to start the email sending process:

```sh
python main.py
```

## File Structure

```
.
├── main.py
├── db_initializer.py
├── database.py
├── .env
├── requirements.txt
└── README.md
```

### main.py
- The main script that handles sending emails.

### db_initializer.py
- Initializes the database and creates the necessary tables if they do not exist.

### database.py
- Contains database table definitions and creation logic.

### .env
- Contains environment variables for email configuration.

### requirements.txt
- Lists the dependencies required for the project.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

Test