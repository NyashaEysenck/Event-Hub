# Django Event Management Web Application

## Overview
This is a Django-based web application for event management. It allows users to register for events, view their registrations, and provide feedback. Superusers can manage events, view all registrations, and download registration data.

## Features
- User registration and authentication
- Event creation and management
- Registration and cancellation of events
- Feedback submission with sentiment analysis
- View and filter registrations
- Download registration data

## Getting Started

### Prerequisites
- Python 3.x
- Django
- Other dependencies listed in `requirements.txt`


### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

To configure the project, you'll need to set up the following environment variables. For development purposes, use a `.env` file in the root of your project.

1. **Create a `.env` file** in the root of your project directory:

    ```bash
    touch .env
    ```

2. **Add the following variables to your `.env` file:**

    ```dotenv
    # Email settings
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.example.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_password
    DEFAULT_FROM_EMAIL=your_email@example.com
    ```

    Replace the placeholder values with your actual email server configuration.

3. **Ensure you have `django-environ` installed:**

    ```bash
    pip install django-environ
    ```

4. **Configure Django to read from the `.env` file:**

    Update your `settings.py` file to use `django-environ`:

    ```python
    import environ

    # Initialize environment variables
    env = environ.Env()
    environ.Env.read_env()  # reads the .env file

    # Email settings
    EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.example.com')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='your_email@example.com')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='your_password')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='your_email@example.com')
    ```

### Running the Development Server

1. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

2. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

3. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

### Testing

To run tests, use:

    ```bash
    python manage.py test


###  Notebooks
The notebooks folder contains Jupyter notebooks for model training and analysis.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Django framework
scikit-learn for machine learning
BeautifulSoup and NLTK for text processing