# Mikro

This minimalistic API service, **Mikro**, is designed for user registration and features a separate mail microservice managed through Kafka messaging. The project leverages **FastAPI** as the main web framework, **SQLAlchemy** for ORM, and **Redis** for caching. It also incorporates various dependencies for handling authentication, asynchronous communication, and logging, making it a foundational setup for microservices-based applications.
## Key Technologies

- **FastAPI**: Web framework for developing the API endpoints.
- **SQLAlchemy**: Database ORM for Python.
- **Redis**: In-memory data structure store for caching.
- **Python-JOSE**: Library for handling JSON Web Tokens (JWT) for authentication.
- **HTTPX**: Async HTTP client for Python.
- **Gunicorn**: HTTP server for running FastAPI in production.
- **Pytest-Twisted**: Testing library used for async code and Kafka integration.
- **AIOKafka**: Kafka client for asynchronous message production and consumption.
- **Sentry SDK**: Tool for monitoring and error tracking.

## Project Structure

- **Core API**: Provides user registration endpoints and handles JWT-based authentication.
- **Mail Microservice**: A separate service for sending emails, decoupled from the main application via Kafka.

## Getting Started

### Prerequisites

Before you start, ensure you have the following installed:

- Docker & Docker Compose
- Make

### Environment Setup

1. Create an `.env` file in the project root directory based on the `.env.example` template:
   ```bash
   cp .env.example .env
   ```

Modify the .env file with your own environment-specific configurations, such as database credentials, Kafka
configuration, and Redis settings.

### Installation & Running the Application

1. Install dependencies using Poetry:

```bash
   poetry install
```

2. To start the application, run:

```bash
   make run
```

This command will start the FastAPI server with Gunicorn.

3. To run the Kafka and Redis services, ensure Docker Compose is configured to start these dependencies. If necessary,
   add the required services to your docker-compose.yml file and start with:

```bash
   docker-compose up -d
```

## Usage

- **API Endpoints**: You can access the API endpoints via [http://localhost:8000](http://localhost:8000). Detailed API
  documentation is available through FastAPI's built-in Swagger
  at [http://localhost:8000/docs](http://localhost:8000/docs).


- **Kafka Integration**: The mail microservice is decoupled from the main API using Kafka messaging. When a user
  registers, a Kafka message is sent to initiate an email through the mail microservice.


## Testing
```bash
   pytest
```


## Monitoring & Error Tracking

The project is set up to use Sentry for error monitoring. Configure Sentry by setting the `SENTRY_DSN` in the `.env` file.
