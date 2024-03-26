from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    User model that extends the default Django User.

    Attributes:
        age (PositiveIntegerField): The age of the user.
        can_be_contacted (BooleanField): Flag to indicate if the user agrees to be contacted. Defaults to False.
        can_data_be_shared (BooleanField): Flag to indicate if the user agrees to share their data. Defaults to False.
        created_time (DateTimeField): The date and time the user was created. Automatically set to the current time when the user is created.
    """

    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Return a string representation of the User.
        """
        return self.username