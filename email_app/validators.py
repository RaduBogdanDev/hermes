from django.core.exceptions import ValidationError
from datetime import datetime


def validate_birthday(value):
    try:
        # Split the date and pad single digits with leading zeros
        day, month = value.split('/')
        day = day.zfill(2)
        month = month.zfill(2)
        formatted_date = f"{day}/{month}"

        # Check if the date is valid
        datetime.strptime(formatted_date, "%d/%m")

        # Update the value to be properly formatted
        value = formatted_date

        # Ensure day and month are correctly formatted
        if day != formatted_date[:2] or month != formatted_date[3:]:
            raise ValidationError("Invalid date format. Use dd/mm format.")
    except ValueError:
        raise ValidationError("Invalid date format. Use dd/mm format.")
    except Exception as e:
        raise ValidationError(str(e))
