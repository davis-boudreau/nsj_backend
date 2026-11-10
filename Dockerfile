FROM python:3.13-slim

# Install system dependencies for GeoDjango (GDAL, GEOS, PROJ)
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Fix: Create a symlink so Django can find the library at the generic path
# This finds whatever version was installed (e.g., 3.6.2) and links it to libgdal.so
RUN ln -s /usr/lib/libgdal.so.* /usr/lib/libgdal.so || true

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src/app

WORKDIR /usr/src/app

RUN python3 -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh \
 && useradd -m -u 10001 cptn_user \
 && chown -R cptn_user:cptn_user /usr/src/app

USER cptn_user
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]