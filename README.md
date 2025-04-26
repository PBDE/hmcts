# HMCTS Case Management System

The HMCTS Case Management System is a Django-based web application designed to manage tasks and cases. It includes features such as user authentication, task creation, task status updates, and task note management.

## Features

- **User Authentication**: Login and logout functionality for secure access.
- **Task Management**: Create, view, update, and delete tasks.
- **Task Status Updates**: Update the status of tasks with predefined options.
- **Task Notes**: Add notes to tasks for better tracking.
- **Responsive Templates**: HTML templates for a user-friendly interface.

## Project Structure

The main files of interest for the purpose of reviewing the code can all be found in the case_management folder:

- **models.py**
- **views.py**
- **tests/functional_tests/test_case_management.py**
- **tests/functional_tests/test_views.py**
- **templates/case_management/*.html**

## Installation

1. Clone the repository:

   git clone https://github.com/PBDE/hmcts/tree/master  
   cd HMCTSCaseManagement
   
2. Set up a virtual environment:

   python -m venv hmcts-env  
   source hmcts-env/bin/activate  # On Windows: hmcts-env\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Set up environment variables: Create a .env file in the hmcts/ directory with the following variables (these variables are for development only):

   SECRET_KEY=<your-secret-key>  
   DEBUG=True  
   ALLOWED_HOSTS=localhost,127.0.0.1  
   SECURE_SSL_REDIRECT=False  
   SECURE_HSTS_SECONDS=0  
   SECURE_HSTS_INCLUDE_SUBDOMAINS=False  
   SECURE_HSTS_PRELOAD=False  
   SESSION_COOKIE_SECURE=False  
   CSRF_COOKIE_SECURE=False  

5. Make migrations:

   py manage.py makemigrations  
   py manage.py migrate

6. Run the development server:

   py manage.py runserver

## Running tests

py manage.py test case_management.tests.unit_tests
py manage.py test case_management.tests.functional_tests


  
