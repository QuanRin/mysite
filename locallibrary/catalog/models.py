import uuid
from datetime import date
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from catalog.constants import GENRE_NAME_MAX_LENGTH, BOOK_TITLE_MAX_LENGTH, BOOK_SUMMARY_MAX_LENGTH, \
    BOOK_ISBN_MAX_LENGTH, BOOK_INSTANCE_IMPRINT_MAX_LENGTH, BOOK_INSTANCE_STATUS_MAX_LENGTH, \
    AUTHOR_FIRST_NAME_MAX_LENGTH, AUTHOR_LAST_NAME_MAX_LENGTH, BOOK_INSTANCE_LOAN_STATUS


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=GENRE_NAME_MAX_LENGTH, help_text=_('Enter a book genre (e.g. Science Fiction)'))

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=BOOK_TITLE_MAX_LENGTH)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=BOOK_SUMMARY_MAX_LENGTH, help_text=_('Enter a brief description of the book'))
    isbn = models.CharField('ISBN', max_length=BOOK_ISBN_MAX_LENGTH, unique=True, help_text=_(
        '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'))
    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = _('Genre')


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text=_('Unique ID for this particular book across whole library'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=BOOK_INSTANCE_IMPRINT_MAX_LENGTH)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = BOOK_INSTANCE_LOAN_STATUS
    status = models.CharField(
        max_length=BOOK_INSTANCE_STATUS_MAX_LENGTH,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        return self.due_back and date.today() > self.due_back


class Author(models.Model):
    first_name = models.CharField(max_length=AUTHOR_FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=AUTHOR_LAST_NAME_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
