from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from projects.models import Project, Contributor
from .models import Issue, Comment


class IssueViewSetTestCase(APITestCase):
    """
    Test suite for the IssueViewSet.

    This class tests the ability to create, retrieve, update, and delete issues within a project,
    while checking the enforcement of permissions and correct project association.
    """

    def setUp(self):
        """
        Sets up necessary data before each test case.

        - Creates two users (one main user and another for testing permissions).
        - Creates a project with the main user as the author.
        - Associates the main user with the project as a contributor.
        """
        self.user = User.objects.create_user(username='user1', password='pass', age=30)
        self.other_user = User.objects.create_user(username='user2', password='pass', age=30)
        self.project = Project.objects.create(title='Test Project', description='Description', type='back-end', author=self.user)
        Contributor.objects.create(user=self.user, project=self.project)
        self.issue_data = {'title': 'Test Issue', 'description': 'Issue Description', 'tag': 'BUG', 'priority': 'LOW'}
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_issue(self):
        """
        Tests if an issue can be successfully created within a project by a project contributor.
        """
        response = self.client.post(reverse('project-issues-list', kwargs={'project_pk': self.project.id}), self.issue_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 1)
        issue = Issue.objects.get()
        self.assertEqual(issue.title, 'Test Issue')

    def test_retrieve_issue_list(self):
        """
        Tests if a project contributor can retrieve the list of issues associated with a project.
        """
        Issue.objects.create(**self.issue_data, author=self.user, project=self.project)
        response = self.client.get(reverse('project-issues-list', kwargs={'project_pk': self.project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # Pagination check
        self.assertEqual(len(response.data['results']), 1)

    def test_non_contributor_cannot_create_issue(self):
        """
        Test ensuring that a non-contributor cannot create an issue in a project.
        """
        # Authenticate with the second user who is not a contributor
        self.client.force_authenticate(user=self.other_user)
        
        # Make a POST request to try creating an issue
        response = self.client.post(reverse('project-issues-list', kwargs={'project_pk': self.project.id}), self.issue_data)
        
        # Assert that the creation is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_author_cannot_modify_issue(self):
        """
        Test ensuring that a user who is not the author of an issue cannot modify it.
        """

        issue = Issue.objects.create(**self.issue_data, author=self.user, project=self.project)
        
        # Authenticate with the second user who is not the author
        self.client.force_authenticate(user=self.other_user)
        
        # Make a PUT request to try modifying the issue
        response = self.client.put(reverse('project-issues-detail', kwargs={'project_pk': self.project.id, 'pk': issue.id}), {'title': 'Unauthorized Title Change'})
        
        # Assert that the modification is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentViewSetTestCase(APITestCase):
    """
    Test suite for the CommentViewSet.

    This class tests the functionality to create, retrieve, and delete comments on issues,
    ensuring that permissions are respected and that comments are associated with the correct issue.
    """

    def setUp(self):
        """
        Sets up the necessary data before each test case.

        - Creates two users (one main user and another for testing permissions).
        - Creates a project and an issue within that project, with the main user as the author.
        - Initializes data for creating a comment.
        """
        self.user = User.objects.create_user(username='user1', password='pass', age=30)
        self.other_user = User.objects.create_user(username='user2', password='pass', age=30)
        self.project = Project.objects.create(title='Test Project', description='Description', type='back-end', author=self.user)
        Contributor.objects.create(user=self.user, project=self.project)
        self.issue = Issue.objects.create(title='Test Issue', description='Issue Description', tag='BUG', priority='LOW', project=self.project, author=self.user)
        self.comment_data = {'text': 'Test Comment'}
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        """
        Tests if a project contributor can successfully create a comment on an issue.
        """
        response = self.client.post(reverse('issue-comments-list', kwargs={'project_pk': self.project.id, 'issue_pk': self.issue.id}), self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get()
        self.assertEqual(comment.text, 'Test Comment')

    def test_retrieve_comment_list(self):
        """
        Tests if a project contributor can retrieve the list of comments associated with an issue.
        """
        # Directly create a comment in the database for testing retrieval
        Comment.objects.create(**self.comment_data, author=self.user, issue=self.issue)
        response = self.client.get(reverse('issue-comments-list', kwargs={'project_pk': self.project.id, 'issue_pk': self.issue.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # Pagination check
        self.assertEqual(len(response.data['results']), 1)

    def test_delete_comment(self):
        """
        Tests if a comment author can delete their comment on an issue.
        """
        # Create a comment to be deleted
        comment = Comment.objects.create(**self.comment_data, author=self.user, issue=self.issue)
        
        # Send a DELETE request to remove the comment
        response = self.client.delete(reverse('issue-comments-detail', kwargs={'project_pk': self.project.id, 'issue_pk': self.issue.id, 'pk': comment.id}))

        # Check the response indicates successful deletion (HTTP 204 status code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Assert that there are no comments left in the database
        self.assertEqual(Comment.objects.count(), 0)

    def test_non_contributor_cannot_create_comment(self):
        """
        Test ensuring that a non-contributor cannot create a comment on an issue.
        """
        # Authenticate as a different user who is not a contributor
        self.client.force_authenticate(user=self.other_user)
        
        # Attempt to create a comment as the non-contributor
        response = self.client.post(reverse('issue-comments-list', kwargs={'project_pk': self.project.id, 'issue_pk': self.issue.id}), self.comment_data)
        
        # Check that the response indicates forbidden access (HTTP 403 status code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_author_cannot_modify_comment(self):
        """
        Test ensuring that a user who is not the author of a comment cannot modify it.
        """
        # Create a comment to test modification attempt
        comment = Comment.objects.create(**self.comment_data, author=self.user, issue=self.issue)
        
        # Switch authentication to a different user
        self.client.force_authenticate(user=self.other_user)
        
        # Attempt to modify the comment using a PUT request as the non-author user
        response = self.client.put(reverse('issue-comments-detail', kwargs={'project_pk': self.project.id, 'issue_pk': self.issue.id, 'pk': comment.id}), {'text': 'Unauthorized Comment Change'})
        
        # Assert that the modification attempt is forbidden (HTTP 403 status code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)