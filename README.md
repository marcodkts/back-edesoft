# Front-End Edesoft

This is a Python project that implements CRUD (Create, Read, Update, Delete) operations using Django API. The project runs in Docker, use Postgres for database and redis for workers queue manager.
The project also can be deployed in AWS enviroment and as a `lambda_handle` for usage.

## Technologies Used

- Python
- Django
- Celery
- Docker
- Redis
- Postgres
- AWS S3
- AWS Lambda

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Run `docker compose up` to start the project.

## Usage

Make sure to check the enviroment variables before running the project for customization.

The links below works when you're running the App via docker. For Django
based authentication, please define your local superuser using the
[createsuperuser](https://docs.djangoproject.com/en/2.2/intro/tutorial02/)
command.

## API endpoints

The following API endpoints are avaiable in the project:

- `/api/Users/` - List all users or create a new user
- `/api/Users/<pk>` - Retrieve, update or delete a user by ID
- `/api/Tasks/ImportCsv/` - Queue a task to import data from S3 to database

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---

| Page                | Address                                                                                                                                  | Use                         | Authenticated |
|:--------------------|:-----------------------------------------------------------------------------------------------------------------------------------------|:----------------------------|:--------------|
| Swagger UI          | [http://localhost:8090/swagger](http://localhost:8090/swagger)   | API Documentation (Swagger) | Yes (Django)  |
| Redoc UI            | [http://localhost:8090/redoc](http://localhost:8090/redoc)       | API Documentation (Redoc)   | Yes (Django)  |
| Django Admin        | [http://localhost:8090/admin](http://localhost:8090/admin)           | Django Admin                | Yes (Django)  |
