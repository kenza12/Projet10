# TaskTracker: Secure RESTful API using Django REST

TaskTracker is an API designed for managing user data, project contributions, issue tracking, and comments within a project management system. It offers a robust way of tracking project progress and facilitates effective communication among contributors.

## Overview

This API focuses on several key aspects of project management:

- **User Management**: Handles user data, privacy, and authentication.
- **Project Management**: Manages project details and contributions.
- **Issue Tracking**: Allows issue creation and tracking within projects.
- **Commenting System**: Enables users to comment on issues for better clarity and collaboration.

## Resources Defined

### User

Defines users with age, consent choices, and credentials.

### Contributor

Links users to specific projects, with capabilities to create Project, Issue, and Comment.

### Project

Represents client application projects, serving as the primary resource.

### Issue

Manages issues within a project, detailing status, priority, assignments, and tags.

### Comment

Allows users to comment on specific issues, enhancing communication.

## Key Features

- **Privacy and Consent Management**: Adherence to privacy norms with consent attributes.
- **User Authentication**: Secure user authentication system with JSON Web Tokens.
- **Project Contributions**: Robust management of user contributions to projects.
- **Issue and Comment Handling**: Efficient tracking and commenting on project issues.

## Installation

Clone the repository:

```shell
git clone https://github.com/kenza12/Projet10.git
cd Projet10
```

Install Pipenv:

```shell
pip install pipenv
```

Install dependencies and activate the virtual environment:

```shell
pipenv install
pipenv shell
```

## Running TaskTracker

To start the server, execute the following command in your terminal:

```shell
python manage.py runserver
```

Once the server is running, you can access the API in several ways:

- **Access via Web Browser:** Navigate to `http://127.0.0.1:8000/` in your web browser. Here, you can interact with the API using the Django REST Framework's browsable interface.
- **Access via Postman:**
    - Open Postman.
    - Set up new requests to interact with the API endpoints.
    - Use `http://127.0.0.1:8000/` as the base URL followed by the specific endpoint paths.
- **Access via Curl:** You can also use curl in the terminal to send requests to the API. For example: `curl -X GET http://127.0.0.1:8000/projects/`.

## API Endpoints and Operations

Each endpoint serves a specific function with defined access permissions.

| Endpoint | Operation | Description | Permission |
|----------|-----------|-------------|------------|
| `/admin/` | CRUD | Admin panel for managing all resources. | Admins only |
| `/signup/` | POST | Endpoint for user registration. | Open to all |
| `/login/` | POST | Endpoint for obtaining JWT token. | Authenticated users |
| `/api/token/refresh/` | POST | Endpoint for refreshing JWT token. | Authenticated users |
| `/users/` | GET | List all users. | Admins only |
| `/users/<int:pk>/` | GET, PUT, DELETE | Retrieve, update, or delete a specific user profile. | Accessible by the user themselves or Admins |
| `/projects/` | POST | Create a projet. | Authenticated users can create projects |
| `/projects/` | GET | List projects created by or contributed to by the authenticated user. | Authenticated users can view projects they've created or contributed to |
| `/projects/<project_pk>/` | GET | Retrieve details of a specific project and its contributors. | Accessible by contributors of the project or the project's author |
| `/projects/<project_pk>/` | PUT, DELETE | Update or delete a specific project | Only the author of the project can update or delete it |
| `/projects/<project_pk>/users/` | POST | Add a contributor to a project. | Only the author of the project can add contributors |
| `/projects/<project_pk>/users/` | GET | List contributors of a specific project. | Accessible by contributors of the project and the project's author |
| `/projects/<project_pk>/users/<users_pk>/` | GET | Retrieve a specific contributor of a project by their ID. | Accessible by contributors of the project and the project's author |
| `/projects/<project_pk>/users/<users_pk>/` | PUT, DELETE | Modify or delete a contributor of a project. | Only the author of the project can modify or delete a contributor |
| `/projects/<project_pk>/issues/` | GET, POST | List issues within a specific project or create new issues. | Accessible by contributors of the project and the project's author |
| `/projects/<project_pk>/issues/<issue_pk>/` | GET | Retrieve specific issue details within a project by issue ID. | Accessible by contributors of the project and the project's author |
| `/projects/<project_pk>/issues/<issue_pk>/` | PUT, DELETE | Update or delete a specific issue within a project. | Only the author of the issue can update or delete it |
| `/projects/<project_pk>/issues/<issue_pk>/comments/` | GET, POST | List comments for a specific issue in a project or create new comments. | Accessible by contributors of the project and the project's author |
| `/projects/<project_pk>/issues/<issue_pk>/comments/<comment_uuid>` | GET | Retrieve a specific comment within a project issue by its unique UUID. | Accessible by contributors of the project and the project's author |
| `/projects/<project_pk>/issues/<issue_pk>/comments/<comment_uuid>` | PUT, DELETE | Update or delete a specific comment within a project issue. | Only the author of the comment can update or delete it |

## Testing

Ensure the API is functioning as intended:

```shell
python manage.py test
```

Tests are available in `tests.py`.

