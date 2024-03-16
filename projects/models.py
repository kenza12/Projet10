from django.db import models
from django.conf import settings
from users.models import User


class Project(models.Model):
    """
    Represents a project within the application.

    Attributes:
        PROJECT_TYPES (tuple): Choices for the type of the project.
        title (CharField): The title of the project.
        description (TextField): A detailed description of the project.
        type (CharField): The type/category of the project.
        author (ForeignKey): A reference to the User who authored and is the main contributor to the project.
        created_time (DateTimeField): The date and time when the project was created, automatically set to now.
    """
    PROJECT_TYPES = (
        ('back-end', 'Back-End'),
        ('front-end', 'Front-End'),
        ('ios', 'iOS'),
        ('android', 'Android')
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=PROJECT_TYPES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the Project, which is its title.
        """
        return self.title

class Contributor(models.Model):
    """
    Intermediary model to represent the many-to-many relationship between User and Project.

    Attributes:
        user (ForeignKey): A reference to the User who is contributing to the project.
        project (ForeignKey): A reference to the Project to which the user is contributing.
        date_joined (DateTimeField): The date and time when the user joined the project as a contributor.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class to define the unique constraint and db table.
        """
        unique_together = ('user', 'project')

    def __str__(self):
        """
        Return a string representation of the Contributor, which is the user's username and the project's title.
        """
        return f"{self.user.username} contributes to {self.project.title}"