
# Social Media API

This project is a backend API for a social media application built with Django and Django REST Framework (DRF). The API allows users to interact with posts, comments, likes, and user accounts.

## Features

- User registration and authentication
- Create, update, and delete posts
- Add comments to posts
- Like and unlike posts
- View lists of liked posts and comments
- API documentation with Swagger

## Prerequisites

- Python 3.11
- Django 5.1.3
- PostgreSQL (or another database, as configured in settings)

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:arsen-arutiunov/social-media-api.git
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database.
   - Update the `DATABASES` settings in `settings.py` with your database credentials.

5. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the API locally at `http://127.0.0.1:8000/api/`.
- View API documentation at `http://127.0.0.1:8000/api/doc/swagger/`.

## Endpoints

### User Authentication

- Register: `POST /api/user/register/`
- Login: `POST /api/user/token/`
- Profile management: `GET /api/user/me/`

### Posts

- List posts: `GET /api/social-media/posts/`
- Create a post: `POST /api/social-media/posts/`
- Update a post: `PUT /api/social-media/posts/<id>/`
- Delete a post: `DELETE /api/social-media/posts/<id>/`

### Comments

- List comments for a post: `GET /api/social-media/posts/<post_id>/comments/`
- Add a comment: `POST /api/social-media/posts/<post_id>/comments/`
- Update a comment: `PUT /api/social-media/comments/<id>/`
- Delete a comment: `DELETE /api/social-media/comments/<id>/`

### Likes

- Like a post: `POST /api/social-media/likes/`
- Unlike a post: `DELETE /api/social-media/likes/<id>/`
- List liked posts: `GET /api/social-media/likes/`

### Test Suite Description

The project includes a comprehensive test suite to ensure the reliability and correctness of the application. The test suite is divided into the following sections:

### 1. Unauthenticated Tests
-	Verifies that API endpoints enforce authentication.
-	Example: Checking that accessing the profile list without authentication returns a 401 Unauthorized response.

### 2. Authenticated Tests
**Profile Tests:**
- Creating, retrieving, and filtering profiles.
- Testing unique constraints (e.g., unique usernames).
- Verifying model properties such as full_name.

**Follow Tests:**
- Creating follows and preventing self-follows.

**Post Tests:**
- Creating posts with and without media files.
- Associating posts with hashtags.

**Hashtag Tests:**
- Creating hashtags.
- Validating relationships between hashtags and posts.

**Like Tests:**
- Liking posts and enforcing unique likes.

**Comment Tests:**
- Creating and editing comments.

**Cascade Deletion Tests:**
- Ensuring related models are correctly deleted when a user is removed.

### 3. Profile Image Upload Tests
- Tests for uploading and managing profile pictures.
- Ensures uploaded images are stored in the correct directory and cleans up after tests.

### 4. Utilities and Helpers
- Reusable utility functions like sample_profile, sample_post, and others to simplify test creation.
