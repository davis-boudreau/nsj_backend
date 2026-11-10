# Journey Web API with Docker and PostgreSQL
---
This project sets up the `stn_api` web API, specifically the `journey` app, using Docker, along with a PostgreSQL database container. It leverages Docker Compose for easy orchestration of these services.

## Prerequisites
---
* Docker and Docker Compose installed on your system.
* Python 3.x installed (if you need to run `manage.py` commands outside of Docker).

## Project Structure
---
```
├── journey/              # Journey web API application code
├── stn_api/              # Django project
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Dockerfile for the web API server
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```
## Getting Started
---
1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd stn_api
    ```

2.  **Start the containers:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images and start the `web` API server and `db` PostgreSQL database containers. The `--build` option ensures that the images are built if they don't exist or if the Dockerfile has changed.

3.  **Access the API:**

    The API server will listen on the localhost, port number `http://localhost:8000`.

## Python `manage.py` Commands (within `web` container)

If you need to execute `manage.py` commands, you can do so within the running `web` container. First, open a shell within the `web` container.

```bash
docker-compose exec web bash
```

Then, run the desired `manage.py` command:

* **Run Migrations:**

    ```bash
    python manage.py migrate
    ```

* **Create Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

* **Run Tests:**

    ```bash
    python manage.py test journey
    ```

* **Run Development Server (If you need to run outside of docker, but docker compose up will do this):**

    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

## Docker Compose Cheatsheet
---
Here are some common Docker Compose commands:

* **Start containers:**

    ```bash
    docker-compose up
    ```

* **Start containers in detached mode (background):**

    ```bash
    docker-compose up -d
    ```

* **Stop containers:**

    ```bash
    docker-compose down
    ```

* **Stop and remove containers, networks, and volumes:**

    ```bash
    docker-compose down -v
    ```

* **Build images:**

    ```bash
    docker-compose build
    ```

* **View container logs:**

    ```bash
    docker-compose logs <service_name>
    ```

    Example: `docker-compose logs web` or `docker-compose logs db`

* **Execute a command inside a running container:**

    ```bash
    docker-compose exec <service_name> <command>
    ```

    Example: `docker-compose exec web python manage.py migrate`

* **List running containers:**

    ```bash
    docker-compose ps
    ```

## Database Access

The PostgreSQL database is accessible from within the `web` container using the following credentials (defined in `docker-compose.yml`):

* **Host:** `db`
* **Port:** `5432`
* **Database:** `postgres`
* **User:** `postgres`
* **Password:** `postgres`

These credentials are for development purposes only. For production, ensure you use secure credentials and environment variables.

## Environment Variables

Environment variables are managed within your `docker-compose.yml` file. For production applications, it is highly recommended to manage these variables through a secure method, and not directly inside of the `docker-compose` file.

## Further Development

* Modify the API code in the `journey/` directory.
* Update dependencies in `requirements.txt`.
* Make changes to the Docker configuration in `docker-compose.yml` or `Dockerfile` as needed.
* Remember to rebuild the images after making changes to `Dockerfile` or `requirements.txt`.

    ```bash
    docker-compose build
    docker-compose up -d
    ```
