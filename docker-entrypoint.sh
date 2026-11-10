#!/bin/bash
set -e

# --- 1. ENVIRONMENT DIAGNOSTICS ---
echo "--- CPTN API Entrypoint ---"
PY=python3
$PY -m pip install --upgrade pip > /dev/null 2>&1

# --- 2. WAIT FOR DATABASE ---
# It's best to do this BEFORE trying to run any migrations or SQL
echo "⏳ Waiting for PostGIS (db) to be ready..."
until $PY manage.py shell -c "from django.db import connection; connection.cursor()" &> /dev/null; do
  sleep 1
done
echo "✅ Database is online."

# --- 3. DEV ONLY: SCHEMA RESET ---
if [ "${RESET_DB:-false}" = "true" ]; then
  echo "⚠️ RESET_DB=true: Dropping and recreating public schema..."
  $PY manage.py dbshell <<'SQL'
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO CURRENT_USER;
GRANT ALL ON SCHEMA public TO public;
SQL
fi

# --- 4. MIGRATIONS ---
# Note: Usually, you don't want 'makemigrations' in an entrypoint for production,
# but for a dev college project, it ensures your code and DB stay in sync.
echo "📦 Running migrations..."
$PY manage.py makemigrations --noinput || true
$PY manage.py migrate --noinput

# --- 5. STATIC FILES ---
# This must happen BEFORE starting the server
if [ "${COLLECTSTATIC:-false}" = "true" ]; then
  echo "📁 Collecting static files..."
  $PY manage.py collectstatic --noinput
fi

# --- 6. SUPERUSER & SEEDING ---
if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
  echo "👤 Creating superuser..."
  $PY create_superuser.py
fi

if [ "${RUN_IMPORTS:-false}" = "true" ]; then
    echo "🚀 RUN_IMPORTS=true: Importing CPTN Data..."
    $PY manage.py import_cptn_data \
        --stops data/stops.csv \
        --areas data/geonames.csv \
        --dist 2
fi

# --- 7. START SERVER ---
# Use exec "$@" so that the command passed from docker-compose.yml 
# (usually 'python manage.py runserver') becomes PID 1.
echo "🚀 Starting Server..."
exec "$@"