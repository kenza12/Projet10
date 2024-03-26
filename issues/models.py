from django.db import models
from projects.models import Project
from users.models import User
import uuid


class Issue(models.Model):
    """
    Represents an issue or task within a project.
    
    Attributes:
        title (CharField): The title of the issue.
        description (TextField): A detailed description of the issue.
        tag (CharField): Categorizes the issue, such as 'Bug', 'Feature', or 'Task'.
        priority (CharField): Priority of the issue, such as 'Low', 'Medium', or 'High'.
        project (ForeignKey): Reference to the project this issue belongs to.
        status (CharField): Current status of the issue, like 'To Do', 'In Progress', or 'Finished'.
        author (ForeignKey): The user who created the issue.
        assignee (ForeignKey): The user who is assigned to work on the issue.
        created_time (DateTimeField): The timestamp when the issue was created.

    Returns:
        string: A string representation of the issue title.
    """
    STATUS_CHOICES = (
        ('TO_DO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )
    TAG_CHOICES = (
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TO_DO')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment made on an issue.

    Attributes:
        id (UUIDField): A unique identifier for the comment. Defaults to a UUID.
        text (TextField): The content of the comment.
        issue (ForeignKey): The issue to which the comment belongs.
        author (ForeignKey): The user who authored the comment.
        created_time (DateTimeField): The timestamp when the comment was made.

    Returns:
        string: A string representation indicating the comment's author and the associated issue title.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"