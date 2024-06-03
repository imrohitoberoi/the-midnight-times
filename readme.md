# News Articles Application

## Overview

This is a Django application for managing and fetching news articles from an external API.

## Features

### User Authentication

Users can log in, and log out.

### Search History

Users can track their search history for news articles.

### Fetch Latest News

The application fetches the latest news articles from external sources in paginated way.

### Keyword Quota

Users have a limit on the number of keywords they can track. Also editable by admin.

### Admin functionalities

Admins can add/block users. Also can see most searched keywords

### Background Tasks

A cronjob which runs hourly to update data for all searched keywords in database to fetch updated results always

## Installation

1. **Clone the repository:**

    ```
    git clone <repository_url>
    ```

2. **Install dependencies in virtual environment & make a .env file using .env.template:**

    ```
    pipenv shell
    pipenv install
    ```

3. **Set up the database [Make sure you have created user and a database with all required permissions]:**

    ```
    python manage.py migrate
    ```

4. **Run the development server:**

    ```
    python manage.py runserver
    ```

5. **Access the application at [http://localhost:8000](http://localhost:8000).**

6. **Run redis server:**

    ```
    sudo systemctl start redis-server
    ```

7. **Run celery backend & celery beat:**

    ```
    celery -A themidnighttimes.celery worker -l info -B
    ```

## Usage

- Create a superuser for django-admin.
- Log in with an existing account.
- Search for news articles using keywords. The search history will be recorded.
- View the latest news articles fetched by the application.
- Admin dashboard for all functionalities.

## Technologies Used

- Django
- Django REST Framework
- MySQL
- Redis
- Celery & Celery Beat


## About the Developer

This project was developed by Rohit Oberoi. 

**Frontend Time Taken:** 17 hours
**Backend Time Taken:** 13 hours
