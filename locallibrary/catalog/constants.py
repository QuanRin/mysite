from enum import Enum

GENRE_NAME_MAX_LENGTH = 200

BOOK_TITLE_MAX_LENGTH = 200
BOOK_SUMMARY_MAX_LENGTH = 200
BOOK_ISBN_MAX_LENGTH = 200

BOOK_INSTANCE_IMPRINT_MAX_LENGTH = 200
BOOK_INSTANCE_STATUS_MAX_LENGTH = 1
PAGINATE_BY = 2
RENEWAL_WEEKS = 3
class LoanStatus(Enum):
    MAINTENANCE = 'm'
    ON_LOAN = 'o'
    AVAILABLE = 'a'
    RESERVED = 'r'

    @classmethod
    def choices(cls):
        """Return a tuple of (value, label) pairs for use in Django models."""
        return tuple((status.value, status.name.capitalize()) for status in cls)

    @classmethod
    def get_label(cls, value):
        """Get the human-readable label for a given value."""
        for status in cls:
            if status.value == value:
                return status.name.capitalize()
        return None

BOOK_INSTANCE_LOAN_STATUS = LoanStatus.choices()

AUTHOR_FIRST_NAME_MAX_LENGTH = 100
AUTHOR_LAST_NAME_MAX_LENGTH = 100
