# Django Authentication System with Reset Password Functionality

This project is a Django-based authentication system that provides essential features like login, registration, password reset via email, and user logout. It also includes validation for forms and displays user-friendly messages for success and error cases.

---

## Features

### 1. **User Authentication**

- Login using a username or email with password authentication.
- Logout functionality to securely end a session.

### 2. **User Registration**

- Create a new account with a first name, last name, username, email, and password.
- Validates form inputs and enforces a minimum password length of 8 characters.
- Prevents duplicate usernames and emails.

### 3. **Forgot Password**

- Allows users to request a password reset link by entering their registered email address.
- Generates a unique reset ID (UUID) and expiration time (5 minutes).
- Sends a reset email with a secure link to reset the password.

### 4. **Password Reset**

- Verifies the reset link (UUID) for validity and checks if it has expired.
- Lets users set a new password, ensuring confirmation matches.

### 5. **Home Page**

- A protected view accessible only to logged-in users.

### 6. **Validation and Messaging**

- Displays form validation errors and success messages using Django's `messages` framework.
- User-friendly error handling for invalid credentials and expired links.

### 7. **Admin Panel and Management**

- The Admin Manages the Entire CRUD for Exam Portal enabling them to `edit` `modify` `delete` or `view` the records of the exam system.
- An user friendly Admin UI is provided inorder to manage the task easily.

---

## Installation

### Prerequisites

- Python 3.8+
- Django 4.0+
- PostgreSQL or SQLite (default)

### Steps

1.  **Clone the repository:**

    ```
    git clone <repository-url>
    cd <project-folder>
    ```

2.  Install Dependencies

    ```
    pip install -r requirements.txt
    ```

3.  Set up the database: Run migrations to initialize the database schema:

    ```
    python manage.py migrate
    ```

4.  Create a superuser:

    ```
    python manage.py createsuperuser
    ```

5.  Run the server: Start the development server:

    ```
    python manage.py runserver
    ```

6.  Access the application: Open your browser and go to:

    ```
    http://127.0.0.1:8000/
    ```

## Usage

### Pages Overview

- Login Page: Located at / (default).
- Registration Page: Available at /signup/.
- Forgot Password Page: Available at /forgot/.
- Reset Password Page: Dynamic URL based on - reset UUID (e.g., /reset/<uuid>/).
- Home Page: Accessible after login at /home/.
  - Admin Home - Enables the admin to manage entire operations for exam.(based on super user).
  - User Home - Enables the student to view their `scores` `records` and `schedules`.

## Environment Variables

Update the `.env` file for sensitive configurations:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-email-password"
SITE_URL=http://127.0.0.1:8000

```

## Project Structure

```
project/
├── templates/               # HTML Templates
|   |── admin
│   ├── index.html           # Login Page
│   ├── signup.html          # Registration Page
│   ├── forgot.html          # Forgot Password Page
│   ├── reset.html           # Reset Password Page
│   ├── home.html            # Home Page
├── static/                  # Static files (CSS, JS, images)
├── authentication/          # Main app for authentication logic
│   ├── views.py             # Core views
│   ├── models.py            # Database models (e.g., ResetID)
│   ├── urls.py              # URL routing for authentication
├── settings.py              # Django settings
└── manage.py                # Django management script
```

## Key Files and Code

### Models

1. ResetID: Stores UUID, user reference, expiration date, and status for password reset requests.

### Views

- Login: Handles login functionality.
- Signup: Manages user registration and validation.
- Forgot: Sends a reset email with a secure UUID link.
- Reset: Validates UUID and expiry time, and allows password reset.
- Logout: Ends user sessions.
- Home: Displays a protected home page for authenticated users.

## Templates

All HTML templates use Bootstrap and custom styling for a responsive and user-friendly UI.

## Validation

- All input fields in forms are validated using HTML attributes and Django backend logic.
- Error and success messages are displayed using Django's `messages` framework.

## Author

Your Name<br>
Email: roshan.khandagale07@gmail.com
