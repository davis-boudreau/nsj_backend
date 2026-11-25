# Journey API local development

Docker Compose runs the Django API, PostgreSQL with PostGIS, and pgAdmin. The separate `nsj_frontend` repository uses Node.js, npm, Vite, and Tailwind.

## 1. Check your tools

Install Git and Docker with the Docker Compose plugin. On Windows or macOS, start Docker Desktop and use Linux containers. Install Node.js with npm if you also plan to run the frontend.

```sh
git --version
docker compose version
docker info
```

Docker builds the backend with Python 3.13 and installs `requirements.txt` inside the image, so the Docker setup needs no host Python installation or virtual environment.

## 2. Clone the repositories

Run these commands from the directory where you keep your projects. Replace the placeholders with your repository URLs. Clone the frontend if you want to run the browser UI.

```sh
git clone "<backend-repository-url>" nsj_backend
git clone "<frontend-repository-url>" nsj_frontend
cd nsj_backend
```

If you already have the repositories, open a terminal in `nsj_backend`, where `docker-compose.yml` lives.

## 3. Create the backend .env file

Create a plain-text file named `.env` beside `docker-compose.yml`. Use the following as a starting point for a new local database. If you already have a working `.env`, keep your existing credentials and make sure `PGADMIN_PORT` differs from 8080.

```dotenv
DEBUG=True
SECRET_KEY=replace-with-a-unique-local-django-secret
ORS_API_KEY=replace-with-your-openrouteservice-key

POSTGRES_DB=cptn_db
POSTGRES_USER=cptn_user
POSTGRES_PASSWORD=replace-with-a-local-database-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

PGADMIN_PORT=8081
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=replace-with-a-local-pgadmin-password

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=replace-with-a-local-django-admin-password
```

- Replace the secret and password placeholders with your own development values. Git ignores `.env`.
- Django requires the `ORS_API_KEY` setting at startup. A placeholder lets you check startup and `/health/`. Routing features need a valid OpenRouteService key.
- Compose uses `db` as the database hostname inside its network. Use `localhost:5432` from a database client running directly on your machine.
- PostgreSQL uses the database name, user, and password when it initializes a new volume. For an existing volume, use its existing credentials.
- Port 8081 keeps pgAdmin separate from the API on port 8080. You can omit the three `DJANGO_SUPERUSER_*` settings and create the account manually later.

## 4. Build and start the backend

From `nsj_backend`, validate the configuration and start the services.

```sh
docker compose config --quiet
docker compose up --build -d
docker compose logs -f cptn_api
```

On startup the API waits for PostGIS, runs Django migrations, creates the configured superuser, and imports the CSV data in `data/`. Wait for the Django development server to start. Press Ctrl+C to exit the log stream. The containers keep running in the background.

To start just the API and its database, use `docker compose up --build -d cptn_api`.

## 5. Verify the backend

- Open [the API health endpoint](http://localhost:8080/health/). It should return JSON containing `"status": "healthy"`.
- Open [Django admin](http://localhost:8080/admin/) and sign in with the Django superuser credentials.
- Open [pgAdmin](http://localhost:8081/) and sign in with the `PGADMIN_DEFAULT_*` credentials. To register the database manually, use host `db`, port `5432`, and the `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` values from `.env`.

`docker compose ps` shows the container status. The current API container health check calls `/api/v1/journey/check-auth/` without a login, which returns HTTP 403. Compose can therefore display `unhealthy` while the API is serving requests. Use `/health/` and the API logs to check startup.

## 6. Start the frontend

Open a second terminal. From `nsj_backend`, switch to the sibling frontend repository, install the locked npm dependencies, and start Vite. On Windows PowerShell, use `npm.cmd` as shown if script execution blocks `npm.ps1`.

```powershell
cd ../nsj_frontend
npm.cmd ci
npm.cmd run dev -- --port 5501 --strictPort
```

On macOS or Linux, use `npm` in place of `npm.cmd`. Open [the local frontend](http://localhost:5501/). Vite processes Tailwind and watches for changes. Port 5501 is already in Django's allowed CORS and trusted CSRF origins for local browser requests.

## Day-to-day commands

Run these commands from `nsj_backend`.

| Task | Command |
| --- | --- |
| Start the backend again | `docker compose up -d` |
| Check service status | `docker compose ps` |
| Follow API and database logs | `docker compose logs -f cptn_api db` |
| Run migrations manually | `docker compose exec cptn_api python manage.py migrate` |
| Create a Django superuser manually | `docker compose exec cptn_api python manage.py createsuperuser` |
| Run Django tests | `docker compose exec cptn_api python manage.py test journey` |
| Rebuild after changing `requirements.txt` or the Dockerfile | `docker compose up --build -d` |
| Shut down and keep the database | `docker compose down` |

Django reloads Python changes from the bind-mounted backend repository. Use `docker compose down -v` only when you intend to delete the local database, pgAdmin state, and collected static files.
