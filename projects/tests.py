from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from .models import Project, Contributor
from django.urls import reverse


class ProjectViewSetTestCase(APITestCase):
    """
    A class for testing the ProjectViewSet. It includes tests for creating projects,
    listing projects, updating, and deleting projects by the project author,
    and ensuring that contributors cannot update or delete projects.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Sets up data used across all tests.
        """
        cls.user = User.objects.create_user(username='testuser', password='12345', age=25)
        cls.project_data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'type': 'back-end'
        }

    def setUp(self):
        """
         Set up executed before each test method. Initializes the APIClient and authenticates the user.
        """
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.other_user = User.objects.create_user(username='otheruser', password='12345', age=30)

    def test_create_project(self):
        """
        Tests if a project can be successfully created and if the creator is automatically added as a contributor.
        """
        response = self.client.post(reverse('project-list'), self.project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.get()
        self.assertEqual(project.title, 'Test Project')
        self.assertTrue(Contributor.objects.filter(user=self.user, project=project).exists())

    def test_list_projects(self):
        """
        Confirms that the logged-in user can see all projects they are associated with,
        both as an author and as a contributor. This test creates two projects: one where the
        user is the author and another where the user is a contributor.
        """
        # Create a project where the logged-in user is the author
        test_project = Project.objects.create(**self.project_data, author=self.user)

        # Create another user and a project where the logged-in user is a contributor
        other_user = User.objects.create_user(username='other', password='12345', age=25)
        other_project = Project.objects.create(title='Other Project', description='Other Description', type='back-end', author=other_user)
        Contributor.objects.create(user=self.user, project=other_project)

        # Perform a GET request to retrieve the list of projects
        response = self.client.get(reverse('project-list'))

        # Check if the response includes a 'results' key (pagination check) and extract the list of projects
        self.assertIn('results', response.data)
        projects_response = response.data['results']

        # Check if both projects (author's project and contributed project) are in the response
        self.assertEqual(len(projects_response), 2)
        project_titles = [project['title'] for project in projects_response]
        self.assertIn(test_project.title, project_titles)
        self.assertIn(other_project.title, project_titles)

    def test_author_can_update_project(self):
        """ Test that the author of a project can update it. """
        # Creating a project with the authenticated user as the author
        project = Project.objects.create(**self.project_data, author=self.user)

        # Data to update the project title
        update_data = {
            'title': 'Updated Title',
            'description': project.description,
            'type': project.type,
        }

        # Sending a PUT request to update the project
        response = self.client.put(
            reverse('project-detail', kwargs={'pk': project.pk}), 
            update_data, 
            format='json'
        )

        # Fetching the updated project to check if the title is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_project = Project.objects.get(pk=project.pk)
        self.assertEqual(updated_project.title, 'Updated Title')

    def test_author_can_delete_project(self):
        """ Test that the author of a project can delete it. """
        project = Project.objects.create(**self.project_data, author=self.user)
        response = self.client.delete(reverse('project-detail', kwargs={'pk': project.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_contributor_cannot_update_or_delete_project(self):
        """  Verifies that a contributor (not the author) of a project cannot update or delete it. """
        # Creating a project with the authenticated user as the author
        project = Project.objects.create(**self.project_data, author=self.user)

        # Adding another user as a contributor to the project
        Contributor.objects.create(user=self.other_user, project=project)

        # Changing the authentication to the contributor
        self.client.force_authenticate(user=self.other_user)

        # Attempting to update the project as the contributor
        update_data = {'title': 'Unauthorized Update'}
        response = self.client.put(reverse('project-detail', kwargs={'pk': project.pk}), update_data)

        # Expecting a 403 Forbidden response as the contributor does not have permission to update
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Attempting to delete the project as the contributor
        response = self.client.delete(reverse('project-detail', kwargs={'pk': project.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ContributorViewSetTestCase(APITestCase):
    """
    This class contains test cases for verifying the functionality of the ContributorViewSet. 
    It specifically tests the ability to add, list, and remove contributors from projects, as well as 
    ensuring that proper permissions are enforced for these actions.
    """

    def setUp(self):
        """
        Initial setup before each test case.
        Here we initialize the APIClient, authenticate the main user, and create another user and a project.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345', age=25)
        self.other_user = User.objects.create_user(username='otheruser', password='12345', age=30)
        self.project = Project.objects.create(title='Test Project', description='Test', type='back-end', author=self.user)
        self.contributor_data = {
            'user': self.other_user.id
        }
        self.client.force_authenticate(user=self.user)

    def test_add_contributor(self):
        """
        Tests adding a contributor to a project.
        """
        response = self.client.post(reverse('project-users-list', kwargs={'project_pk': self.project.id}), self.contributor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_contributors(self):
        """
        Tests listing the contributors of a project.
        """
        Contributor.objects.create(user=self.other_user, project=self.project)
        response = self.client.get(reverse('project-users-list', kwargs={'project_pk': self.project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_contributor(self):
        """
        Tests the removal of a contributor from a project.
        """
        contributor = Contributor.objects.create(user=self.other_user, project=self.project)
        url = f"/projects/{self.project.id}/users/{contributor.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission_denied_non_author(self):
        """
        Tests that non-authors (contributors) are denied permission to add other contributors.
        """
        # Authenticate as the other user (not the author)
        self.client.force_authenticate(user=self.other_user)

        # Attempt to add a contributor as the non-author user
        response = self.client.post(reverse('project-users-list', kwargs={'project_pk': self.project.id}), self.contributor_data)
        
        # Asserting that the non-author user is denied permission (status code 403)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)