# SUTHUB PYTHON DEVELOPER APPLICATION TEST

The Age Groups and Enrollments API is a RESTful web service built with FastAPI, designed to manage age groups and enrollments for a system. The API allows users to define age groups with minimum and maximum age ranges and register enrollments with their name, age, and CPF (Cadastro de Pessoas Físicas, a Brazilian national identification number), its destined for the review of the hiring and technical team of SUTHUB


## Features

Age Groups Management: Define age groups with specific age ranges.
Enrollment Registration: Register enrollments with name, age, and CPF.
Authentication: Basic authentication for securing API endpoints.
Queue Processing: Enrollments are queued for processing before being stored in the database.

## Technologies Used

Python 3.11
FastAPI: Web framework for building APIs with Python.
MongoDB: NoSQL document database for storing age groups and enrollments.
Redis: In-memory data structure store used as a message broker for queueing enrollments.
Docker: Containerization platform for deploying and running the API in isolated environments.

## Installation

1. Clone the repository:

    ```bash
    git clone repository-url
    cd repository-name
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    The use of a Virtual Env is recommended for this case

## Configuration

1. Create a `.env` file and paste it inside enrollments/app , age_groups/app, tests folder and processor:

    ```plaintext
    MONGO_URI=mongodb://<username>:<password>@<host>:<port>/<database>
    REDIS_URI=redis://<host>:<port>/<db>
    BASIC_AUTH_USERNAME=<username>
    BASIC_AUTH_PASSWORD=<password>
    ```

    Replace placeholders with your MongoDB and Redis connection URIs, as well as basic authentication credentials.

## Usage

1. Run the API:

    ```bash
    docker-compose up --build
    ```

2. The API will be available at:

    - Age Groups API: `http://localhost:8000`
    - Enrollments API: `http://localhost:8001`

## API Endpoints

- Age Groups API:
  - `POST /age-groups/`
  - `GET /age-groups/`
  - `GET /age-groups/{id}/`
  - `PUT /age-groups/{id}/`
  - `DELETE /age-groups/{id}/`
  - `DELETE /age-groups/clear`

- Enrollments API:
  - `POST /enrollments/`
  - `GET /enrollments/`
  - `PUT /enrollments/{id}/`
  - `DELETE /enrollments/{id}/`
  - `DELETE /enrollments/clear`

## Testing

Run tests using pytest:

```bash
pytest age_groups/tests
pytest enrollments/tests
