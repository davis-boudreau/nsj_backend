## **Project Setup 01: stn_backend - Robust and Scalable API for Location Data**

**1. Development Environment Preparation**
---

### 1. Install Visual Studio Code (VS Code)
   1. Visit the official Visual Studio Code website: [https://code.visualstudio.com/](https://code.visualstudio.com/).
   2. Download the appropriate installer for your operating system.
   3. Run the installer and follow the installation prompts.

### 2. Install Python
   - **For Windows:**
     1. Go to [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/).
     2. Download the latest Python installer.
     3. During the installation process, check the **"Add Python to PATH"** option.
   - **For Linux (Ubuntu/Debian):**
     1. Open a terminal.
     2. Update your system packages by running:
        ```bash
        sudo apt update
        ```
     3. Install Python and pip using the command:
        ```bash
        sudo apt install python3 python3-pip
        ```

### 3. Install Docker
   - **For Windows:**
     1. Visit the Docker Desktop page: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
     2. Download and run the Docker Desktop installer.
     3. Follow the setup instructions to complete the installation.
   - **For Linux (Ubuntu/Debian):**
     1. Open a web browser and navigate to the official Docker installation guide: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/).
     2. Follow the step-by-step instructions provided there.


### 4. Upgrade Python, pip, and setuptools
   - To avoid compatibility issues with outdated tools:
     1. Open a terminal or command prompt.
     2. Run the following command to upgrade pip, setuptools, and the wheel:
        ```bash
        python -m pip install --upgrade pip setuptools wheel
        ```

--- 

**2. Setting Up the Project**
---

#### 1: Create the Project Directory
1. Choose a name for your project folder, such as `stn_backend`.
2. Create the directory using your file explorer or terminal/command prompt.
3. Launch Visual Studio Code and open the newly created directory.

#### 2: Create a Virtual Environment
1. Open the terminal inside VS Code (for Windows users, ensure the terminal type is set to Command Prompt).
2. Create the virtual environment by running the appropriate command:
   - **Linux/macOS:**
     ```bash
     python3 -m venv venv
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     ```
3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```

**3. Install Packages and Frameworks**
---

#### Step 1: Key Packages and Their Purpose
- **Django**: A robust Python web framework for building secure, scalable applications, offering features like database handling, routing, and user authentication.
- **Django Rest Framework (DRF)**: Simplifies API creation with tools for serialization, authentication, and permissions.
- **Psycopg**: A PostgreSQL adapter for Python that facilitates advanced database operations.
- **python-decouple**: Manages application settings securely by storing configuration variables in a `.env` file.
- **Celery**: A task queue system for running background jobs, such as sending emails or processing data.
- **Redis**: An in-memory data store, ideal for caching or messaging, often used with Celery for task handling.
- **Pandas**: Provides efficient tools for data analysis and manipulation, particularly with tabular data.

#### Step 2: Create a `requirements.txt` File
1. In the root of your project directory, create a file named `requirements.txt`.
2. Include the following packages in the file:
   ```text
   Django
   djangorestframework
   psycopg
   python-decouple
   celery
   redis
   pandas
   ```

#### Step 3: Install the Packages
1. Open your terminal.
2. Use the following command to install all the packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
---

**4. Create the `.env` File**
---

#### Why Use a `.env` File?
1. **Centralized Configuration**: By centralizing all sensitive details like database credentials in a `.env` file, both your Django application and Docker setup can easily access consistent settings.
2. **Automatic Loading in Docker**: The `env_file` directive in `docker-compose.yml` ensures Docker Compose can read environment variables directly from your `.env` file. This removes the need to manually specify variables like `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` inside the Compose file.
3. **Simplified Updates**: Any future changes to your environment variables can be made in one place—the `.env` file—without modifying multiple configuration files.

#### What Role Does `python-decouple` Play?
- `python-decouple` is a Python library that simplifies loading environment variables stored in a `.env` file into your Django project.
- Instead of hardcoding sensitive information like database credentials or secret keys in your Django settings file, you can use `python-decouple` to securely access these values from the `.env` file.
- This keeps your codebase clean and makes it more secure by avoiding the exposure of sensitive details in your source code repository.

#### Steps to Create and Use the `.env` File
1. **Create the `.env` File**:
   - In the **root directory** of your project, create a file named `.env`. For example:
     ```
     ├── your_project/
         ├── .env
         ├── manage.py
         ├── docker-compose.yml
         ├── your_app/
         ├── ...
     ```
2. **Add Environment Variables**:
   - In the `.env` file, add database credentials and other necessary variables:
     ```text
     POSTGRES_DB=stn_db
     POSTGRES_USER=stn_user
     POSTGRES_PASSWORD=3P7JDW2$
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     POSTGRES_INITDB_ARGS=--encoding=UTF8 --auth=scram-sha-256
     SECRET_KEY=your_django_secret_key
     DEBUG=True
     ```

3. **Configure Django to Use `python-decouple`**:
   - Install `python-decouple` if you haven’t already:
     ```bash
     pip install python-decouple
     ```
   - Update your Django `settings.py` file to use `python-decouple` to load environment variables. Example:
     ```python
     from decouple import config

     SECRET_KEY = config('SECRET_KEY')
     DEBUG = config('DEBUG', default=False, cast=bool)
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': config('POSTGRES_DB'),
             'USER': config('POSTGRES_USER'),
             'PASSWORD': config('POSTGRES_PASSWORD'),
             'HOST': config('POSTGRES_HOST'),
             'PORT': config('POSTGRES_PORT'),
         }
     }
     ```

---

### 5. **Configuring PostgreSQL in Docker**

#### Update Your `docker-compose.yml` File
- Adjust the `docker-compose.yml` file to utilize the `.env` file for environment variables. This ensures your configuration remains flexible and secure. Example configuration:

```yaml
services:
  db:
    image: postgres:latest
    container_name: postgres_container
    env_file: .env  # Load environment variables from .env file
    ports:
      - "5432:5432"  # Expose PostgreSQL on port 5432
    volumes:
      - db_data:/var/lib/postgresql/data/  # Persist database data

volumes:
  db_data:  # Define a volume to retain database data
```

**6. Implement a `.gitignore` File**
---

#### Why Use `.gitignore`?
- **Protect Sensitive Information**: `.gitignore` ensures files like `.env`, which contain sensitive data (e.g., API keys, database credentials), are excluded from version control. This protects them from being accidentally exposed when sharing the project on platforms like GitHub.
- **Reduce Clutter**: It prevents unnecessary or temporary files (e.g., logs, compiled binaries) from being tracked in your repository, keeping your codebase clean and focused on essential files.
- **Streamline Collaboration**: By excluding irrelevant files, `.gitignore` helps collaborators focus only on the files critical to the project's functionality.

---

#### Steps to Implement `.gitignore`

##### Step 1: Create a `.gitignore` File
1. Navigate to the **root directory** of your project.
2. Check if a `.gitignore` file already exists. If not, create one by running:
   ```bash
   touch .gitignore
   ```

---

##### Step 2: Add `.env` to `.gitignore`
1. Open the `.gitignore` file using a text editor. For example:
   ```bash
   nano .gitignore
   ```
2. Add the following line to exclude the `.env` file:
   ```
   # Ignore environment variables file
   .env
   ```
3. Save and close the file.

---

##### Step 3: Remove `.env` from Git (If Previously Tracked)
- If the `.env` file was accidentally added to version control, remove it from the Git index while keeping it locally:
   ```bash
   git rm --cached .env
   ```
- This command ensures `.env` stays on your local machine but is no longer tracked by Git.

---

##### Step 4: Commit Changes
1. Stage the updated `.gitignore` file:
   ```bash
   git add .gitignore
   ```
2. Commit the changes:
   ```bash
   git commit -m "Add .env to .gitignore"
   ```

---

##### Step 5: Verify the Changes
1. Run the following command to check Git's status:
   ```bash
   git status
   ```
2. Ensure the `.env` file is no longer displayed as a tracked or untracked file.

---

**7. Starting the PostgreSQL Container:**
---
  **In the VS Code terminal run:** 
   ```bash
    docker-compose up -d db
   ```

### **Stopping PostgreSQL Container:**
   **In the VS Code terminal run:**
   ```bash
    docker-compose down
   ```
### **Stopping PostgreSQL Container and Removing the Docker Volume:**
   **In the VS Code terminal:**
   ```bash
    docker-compose down -v
   ```

### Testing Connection to PostgreSQL (Requires local installation of postgres)

1. Confirm the connection to your PostgreSQL database using the credentials provided. Execute the following command:
 ```bash
   psql -h 127.0.0.1 -U stn_user -d stn_db
 ```
   When prompted, input the password (`stn_password`).

2. If the connection fails, review the database credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) in your `docker-compose.yml` file to ensure they are accurate.  If using .env, please ensure the environment variables are correct.

3. After correcting any errors, restart the container to apply the changes:
 ```bash
   docker-compose down -v
   docker-compose up -d
 ```
---

**8. Django API Server (Journey App)**
---

#### **Step 1: Create a Django Project**
1. Open the VS Code terminal.
2. Run the following command to create a new Django project:
   ```bash
   django-admin startproject stn_project .
   ```

---

#### **Step 2: Create a Django App**
1. Create a new app named `journey` by running:
   ```bash
   python manage.py startapp journey
   ```

---

#### **Step 3: Configure Installed Apps**
1. Open `stn_project/settings.py`.
2. Add `'rest_framework'` and `'journey'` to the `INSTALLED_APPS` list:
   ```python
   INSTALLED_APPS = [
       # Other apps
       'rest_framework',
       'journey',
   ]
   ```

---

#### **Step 4: Configure the Database with `python-decouple`**

##### Why Use `python-decouple`?
- `python-decouple` enhances security and flexibility by enabling Django to load database credentials and other sensitive data from the `.env` file, rather than hardcoding them in the `settings.py` file.

##### Steps:
1. Install `python-decouple`:
   ```bash
   pip install python-decouple
   ```
2. In your `.env` file, define the PostgreSQL environment variables typically used:
   ```text
   POSTGRES_DB=stn_db
   POSTGRES_USER=stn_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

3. Update the `DATABASES` configuration in `stn_project/settings.py` to reference these environment variables:
   ```python
   from decouple import config

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': config('POSTGRES_DB'),
           'USER': config('POSTGRES_USER'),
           'PASSWORD': config('POSTGRES_PASSWORD'),
           'HOST': config('POSTGRES_HOST'),
           'PORT': config('POSTGRES_PORT'),
       }
   }

   SECRET_KEY = config('SECRET_KEY')
   DEBUG = config('DEBUG', default=False, cast=bool)
   ```

---

**9. Create the `Location` Model**
---

```python
from django.db import models

class Location(models.Model):
    # Unique identifier for the location
    OBJECTID = models.IntegerField(primary_key=True)
    
    # Name of the geographical location
    GEONAME = models.CharField(max_length=255)
    
    # County in which the location is found
    COUNTY = models.CharField(max_length=255)
    
    # Latitude based on the NAD83 datum
    NAD83_LAT = models.FloatField()
    
    # Longitude based on the NAD83 datum
    NAD83_LON = models.FloatField()
    
    # Narrative description of the location
    LOCN_NARR = models.TextField()

    def __str__(self):
        # String representation of the model object
        return self.GEONAME
```

**10. Create Serializer (`journey/serializers.py`)**
---
```python
from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'OBJECTID',
            'GEONAME',
            'COUNTY',
            'NAD83_LAT',
            'NAD83_LON',
            'LOCN_NARR'
        ]
```

---

**11. Create View (`journey/views.py`)**
---
```python
from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer

class LocationList(generics.ListAPIView):
    """
    API view to retrieve a list of Location objects.
    """
    queryset = Location.objects.all()  # Retrieves all location entries
    serializer_class = LocationSerializer  # Specifies the serializer to use
```

---

**12. Create URLs (`journey/urls.py`)**
---

```python
from django.urls import path
from .views import LocationList

urlpatterns = [
    path('locations/', LocationList.as_view(), name='location-list'),
]
```

---

**13. Include URLs in `stn_project/urls.py`**
---

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # URL pattern for the admin interface
    path('admin/', admin.site.urls),
    
    # Include the URLs from the 'journey' app under the 'api/' prefix
    path('api/', include('journey.urls')),
]
```

---

**14. Migrate Database:**
---
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

---

**15. Run Django in Docker**
---
### 1. Add Django Service to `docker-compose.yml`

```yaml
services:
  db:
    # Configuration for the database service
    # ... previous db configuration

  web:
    build: .  # Build from the current directory
    command: python manage.py runserver 0.0.0.0:80  # Run the Django development server
    volumes:
      - .:/app  # Mount the project directory into the container
    ports:
      - "80:80"  # Map port 8000 on the host to port 8000 on the container
    depends_on:
      - db  # Ensure the 'db' service is started before 'web'
```

---

### 2. Create `Dockerfile` in the Root of the Project

```dockerfile
# Use the official Python 3.9 slim image as the base
FROM python:3.13.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the dependencies specified in the requirements file
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/
```

---

**16. Build and Run the Docker Containers**
---

```bash
docker-compose up --build
```

---
**17. Import Utility**
---
#### Create `import_data.py` in the Root of the Project

```python
import psycopg
import csv
from decouple import config

def import_data(csv_file):
    """
    Import data from a CSV file into the PostgreSQL database using Psycopg 3
    and environment variables from a .env file.
    """
    try:
        # Establish a connection to the database using environment variables from the .env file
        with psycopg.connect(
            dbname=config("POSTGRES_DB"),
            user=config("POSTGRES_USER"),
            password=config("POSTGRES_PASSWORD"),
            host=config("POSTGRES_HOST"),
            port=config("POSTGRES_PORT")
        ) as conn:
            with conn.cursor() as cur:
                # Open the CSV file and read its contents
                with open(csv_file, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the header row

                    # Insert rows from the CSV file into the database
                    for row in reader:
                        cur.execute("""
                            INSERT INTO journey_location (OBJECTID, GEONAME, COUNTY, NAD83_LAT, NAD83_LON, LOCN_NARR)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, row)

            # Commit the transaction to save changes in the database
            conn.commit()
            print("Data imported successfully.")

    except psycopg.Error as e:
        # Print any database-related errors
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace 'your_data.csv' with the name of your CSV file
    import_data('your_data.csv')
```

---

### Example `.env` File:

Create a `.env` file in the root directory of your project and include the following environment variables:

```env
POSTGRES_DB=stn_db
POSTGRES_USER=stn_user
POSTGRES_PASSWORD=3P7JDW2$
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

### Notes:
- **Uses `python-decouple`:**
   Ensure python-decouple is in the `requirements.txt`
   To manually install python-decouple (not required if using `requirements.txt`):
   ```bash
   pip install python-decouple
   ```

- **Ensure Proper Configuration:**
   Make sure the `.env` file is in the same directory as the script.

---

**18. Execute the Data Import Script**
---

Run the following command in your terminal to execute the script:

```bash
python import_data.py
```

---

**19. Test the API Query**
---

#### Option 1: Using `curl` (Command Line)

1. Open your terminal.
2. Execute the following command to test the API endpoint:

```bash
curl -X GET http://localhost:80/api/locations/
```

3. **Expected Response:** You should see a JSON response in your terminal that contains the data from your `journey_location` table, similar to:

```json
[
    {
        "OBJECTID": 1,
        "GEONAME": "Example Location",
        "COUNTY": "Example County",
        "NAD83_LAT": 45.12345,
        "NAD83_LON": -60.12345,
        "LOCN_NARR": "Sample location narrative."
    },
    {
        "OBJECTID": 2,
        "GEONAME": "Another Location",
        "COUNTY": "Another County",
        "NAD83_LAT": 46.67890,
        "NAD83_LON": -61.67890,
        "LOCN_NARR": "Another sample narrative."
    }
]
```

---

#### Option 2: Using Postman

1. **Install Postman**  
   - If Postman isn't installed, download it from [Postman’s official website](https://www.postman.com/downloads/) and install it.

2. **Create a New Request**
   - Launch Postman and click the “+” or “New Request” button.

3. **Set Up the Request**
   - Choose `GET` as the method from the dropdown menu.
   - Enter the URL: `http://localhost:80/api/locations/`.

4. **Optional: Add Headers**
   - If your API requires specific headers (e.g., for authentication), add them by clicking on the "Headers" tab.
   - Example header:  
     ```
     Key: Authorization  
     Value: Bearer <your-token>
     ```

5. **Send the Request**
   - Click “Send” to make the API call.

6. **Check the Response**
   - The response will appear in the lower section of Postman, displaying the JSON data retrieved from your `journey_location` table.

---

### Troubleshooting
- **Ensure Django is Running:**  
  Make sure the Django server is active. Start it by running:

  ```bash
  python manage.py runserver
  ```

- **Verify Endpoint:**  
  Double-check the URL to ensure it matches your setup.

---

**Pagination, Filtering, and Sorting**
---

**20. Pagination:**
---
Pagination helps manage large datasets by dividing them into smaller chunks (pages). Django REST Framework (DRF) provides built-in classes for implementing pagination, such as `PageNumberPagination` and `LimitOffsetPagination`. Here’s how to implement pagination in your project:

---

### Step 1: Define a Custom Pagination Class
Create a pagination class to specify the number of items per page and additional options like `max_page_size`:

```python
from rest_framework.pagination import PageNumberPagination

class LocationPagination(PageNumberPagination):
    """
    Custom pagination class for the Location model.
    """
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Parameter to set page size dynamically
    max_page_size = 100  # Limit the maximum number of items per page
```

---

### Step 2: Integrate Pagination into the View

In the `journey/views.py` file, add the custom pagination class to the `LocationList` view:

```python
from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer
from .pagination import LocationPagination  # Import the custom pagination class

class LocationList(generics.ListAPIView):
    """
    API view to retrieve paginated Location objects.
    """
    queryset = Location.objects.all()  # Fetch all location entries
    serializer_class = LocationSerializer  # Specify the serializer for data
    pagination_class = LocationPagination  # Apply the custom pagination class
```

---

### Step 3: Test Pagination with the Endpoint

1. Start your Django server using:
   ```bash
   python manage.py runserver
   ```

2. Access the API endpoint, e.g., `http://localhost:8000/api/locations/`.

3. You’ll receive a paginated response like the following:

```json
{
    "count": 50,  // Total number of objects
    "next": "http://localhost:8000/api/locations/?page=2",  // URL for the next page
    "previous": null,  // URL for the previous page (null if you're on the first page)
    "results": [
        {
            "OBJECTID": 1,
            "GEONAME": "Example Location",
            "COUNTY": "Example County",
            "NAD83_LAT": 45.12345,
            "NAD83_LON": -60.12345,
            "LOCN_NARR": "Sample location narrative."
        },
        // Additional objects here
    ]
}
```

---

### Additional Pagination Details

#### **Dynamic Page Size:**
By using the `page_size_query_param`, clients can dynamically set the page size:
```http
http://localhost:8000/api/locations/?page_size=5
```
This query adjusts the number of objects per page dynamically.

---

#### **Alternatives to PageNumberPagination:**
If you prefer a different pagination approach, you can use `LimitOffsetPagination`, which allows clients to specify an offset and limit:
```python
from rest_framework.pagination import LimitOffsetPagination

class LocationPagination(LimitOffsetPagination):
    default_limit = 10  # Number of items per page
    max_limit = 100  # Limit the maximum items per page
```

---

### Step 4: Extend Pagination to Other Views

To apply pagination globally across all API views, modify the `settings.py` file in your project:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Default page size for all views
}
```

---

### Benefits of Pagination:
1. **Improved Performance:** Reduces data transferred in a single response, improving performance.
2. **Customizability:** Allows flexible pagination methods and page sizes.
3. **Scalability:** Efficiently handles large datasets without overwhelming clients.

---

**21. Filtering in Django REST Framework**
---

Filtering allows clients to retrieve data that matches specific criteria, reducing the volume of unnecessary information. Django Filters is a powerful tool for adding filtering capabilities to your API. Follow the steps below to implement filtering in your project.

---

### **Step 1: Install Dependencies**
1. Install the `django-filter` package:
   ```bash
   pip install django-filter
   ```

2. Add `'django_filters'` to the `INSTALLED_APPS` list in your `stn_project/settings.py`:
   ```python
   INSTALLED_APPS = [
       # Other apps
       'django_filters',
   ]
   ```

---

### **Step 3: Apply Filtering in the View**

Update the `LocationList` view in `journey/views.py` to include filtering. Define the fields you want clients to filter by:

```python
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Location
from .serializers import LocationSerializer
from .pagination import LocationPagination

class LocationList(generics.ListAPIView):
    """
    API view for paginated and filtered Location objects.
    """
    queryset = Location.objects.all()  # Fetch all location entries
    serializer_class = LocationSerializer  # Use the Location serializer
    pagination_class = LocationPagination  # Apply pagination
    filter_backends = [DjangoFilterBackend]  # Enable filtering
    filterset_fields = ['COUNTY', 'GEONAME']  # Define the fields for filtering
```

Here:
- **`filter_backends`** specifies the filtering mechanism used in the view (`DjangoFilterBackend`).
- **`filterset_fields`** lists the model fields (`COUNTY`, `GEONAME`) available for filtering.

---

### **Step 4: Test Filtering**

1. **Start the Django Development Server:**
   ```bash
   python manage.py runserver
   ```

2. **Test Filtering with API Requests:**
   - Use query parameters to filter results by specific fields:
     ```http
     http://localhost:8000/api/locations/?COUNTY=ExampleCounty
     http://localhost:8000/api/locations/?GEONAME=ExampleLocation
     ```

3. **Combine Filters:**
   Apply multiple filters simultaneously to narrow down results further:
   ```http
   http://localhost:8000/api/locations/?COUNTY=ExampleCounty&GEONAME=ExampleLocation
   ```

---

### **Step 5: Optional - Global Configuration**

If you want filtering enabled globally across all views in your project, modify the `REST_FRAMEWORK` settings in `stn_project/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Default page size
}
```

This ensures all views with a `queryset` support filtering and pagination without requiring individual configuration.

---

### **Expected Responses**

1. **Filtered Response Example:**
   A response filtered by the specified query parameters:
   ```json
   [
       {
           "OBJECTID": 1,
           "GEONAME": "Example Location",
           "COUNTY": "Example County",
           "NAD83_LAT": 45.12345,
           "NAD83_LON": -60.12345,
           "LOCN_NARR": "Sample location narrative."
       }
   ]
   ```

2. **Combined with Pagination:**
   Filtering works seamlessly with pagination, showing the filtered results in pages.

### **Key Benefits of Filtering**
- **Flexibility:** Allows clients to retrieve tailored datasets.
- **Efficiency:** Reduces data transfer overhead by filtering unnecessary information.
- **Scalability:** Handles large datasets while providing focused results.

---

**22. Sorting in Django REST Framework**

Sorting allows clients to order results based on specific fields, enhancing the flexibility and usability of the API. Django REST Framework provides the `OrderingFilter`, which makes implementing sorting straightforward. Follow the steps below for integration.

---

### **Step 1: Install Dependencies**

If you haven't already installed Django Filters for filtering support, follow these steps:
1. Install `django-filter`:
   ```bash
   pip install django-filter
   ```

2. Add `'django_filters'` to `INSTALLED_APPS` in your `stn_project/settings.py`:
   ```python
   INSTALLED_APPS = [
       # Other apps
       'django_filters',
   ]
   ```

This ensures compatibility with filtering and sorting features.

---

### **Step 2: Define a Pagination Class**

Sorting works seamlessly with pagination, so defining a pagination class can optimize result management:

```python
from rest_framework.pagination import PageNumberPagination

class LocationPagination(PageNumberPagination):
    """
    Custom pagination class for paginating Location objects.
    """
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to specify page size dynamically
    max_page_size = 100  # Limit the maximum page size
```

---

### **Step 3: Add Sorting in the View**

Use the `OrderingFilter` in combination with filtering and pagination. Update the `LocationList` view in `journey/views.py`:

```python
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Location
from .serializers import LocationSerializer
from .pagination import LocationPagination

class LocationList(generics.ListAPIView):
    """
    API view for paginated, filtered, and sorted Location objects.
    """
    queryset = Location.objects.all()  # Fetch all location entries
    serializer_class = LocationSerializer  # Use the Location serializer
    pagination_class = LocationPagination  # Apply pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Enable filtering and sorting
    filterset_fields = ['COUNTY', 'GEONAME']  # Specify fields available for filtering
    ordering_fields = ['GEONAME', 'COUNTY', 'OBJECTID']  # Specify fields for sorting
```

Here:
- **`filter_backends`** combines `DjangoFilterBackend` (for filtering) and `OrderingFilter` (for sorting).
- **`ordering_fields`** lists the model fields (`GEONAME`, `COUNTY`, `OBJECTID`) available for sorting.

---

### **Step 4: Test Sorting**

1. **Start the Django Development Server:**
   ```bash
   python manage.py runserver
   ```

2. **Test Sorting with API Requests:**
   - Sort results by a specific field using the query parameter `ordering`:
     ```http
     http://localhost:8000/api/locations/?ordering=GEONAME
     ```
   - Sort results in descending order by adding a minus sign (`-`) before the field name:
     ```http
     http://localhost:8000/api/locations/?ordering=-COUNTY
     ```

3. **Combine Sorting with Pagination and Filtering:**
   - Sorting works alongside pagination and filtering:
     ```http
     http://localhost:8000/api/locations/?ordering=GEONAME&COUNTY=ExampleCounty&page=2
     ```

---

### **Step 5: Optional - Global Configuration**

If you want sorting enabled globally across all views, modify the `REST_FRAMEWORK` settings in `stn_project/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Set the default page size
}
```

This ensures sorting is available for all views with a `queryset`.

---

### **Expected Responses**

1. **Sorted Response Example:**
   A response ordered by the specified field (e.g., `GEONAME`):
   ```json
   [
       {
           "OBJECTID": 1,
           "GEONAME": "Example Location A",
           "COUNTY": "County X",
           "NAD83_LAT": 45.12345,
           "NAD83_LON": -60.12345,
           "LOCN_NARR": "Sample narrative."
       },
       {
           "OBJECTID": 2,
           "GEONAME": "Example Location B",
           "COUNTY": "County Y",
           "NAD83_LAT": 46.67890,
           "NAD83_LON": -61.67890,
           "LOCN_NARR": "Another narrative."
       }
   ]
   ```

2. **Combined with Filtering and Pagination:**
   Filtering and pagination complement sorting for better data management.

---

### **Benefits of Sorting**
- **Flexibility:** Provides dynamic control over how data is ordered.
- **Improved Usability:** Enables clients to retrieve results tailored to their requirements.
- **Integration:** Works seamlessly with filtering and pagination for comprehensive functionality.

---

**23. Error Handling in Django REST Framework**
---
Error handling is crucial for delivering meaningful feedback to API clients. Properly structured error responses enhance usability, improve debugging, and ensure consistency. Below are detailed steps to implement robust error handling.

---

### **Step 1: Customize Exception Responses in `settings.py`**

You can define a global exception handler to manage error responses across your project. Update the `stn_project/settings.py` file to include the following configuration:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'stn_project.exceptions.custom_exception_handler',
}
```

Here, `custom_exception_handler` is a function that you will define to control how exceptions are handled.

---

### **Step 2: Create a Custom Exception Handler**

Create a new file called `exceptions.py` in your project directory (`stn_project/`), and define a custom exception handler:

```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler that modifies error responses.
    """
    # Call the default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the default error response
        response.data['status_code'] = response.status_code
    else:
        # Handle any unhandled exceptions
        response = Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
```

---

### **Step 3: Add Specific Error Handling in Views**

In individual views, catch and handle exceptions specific to your logic. Here’s how to modify your `LocationList` view in `journey/views.py`:

```python
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import FieldError, ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from .models import Location
from .serializers import LocationSerializer
from .pagination import LocationPagination

class LocationList(generics.ListAPIView):
    """
    API view to retrieve paginated and filtered Location objects with error handling.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = LocationPagination

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except FieldError as fe:
            # Handle invalid filter or sort field names
            return Response(
                {'error': str(fe), 'message': 'Invalid filter or sort field.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as ve:
            # Handle invalid page or page size values
            return Response(
                {'error': str(ve), 'message': 'Invalid page number or page size.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as ve:
            # handle invalid data within the filter parameters.
            return Response(
                {'error': str(ve), 'message': 'Invalid data in filter parameters.'},
                status = status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # Handle unexpected errors
            return Response(
                {'error': str(e), 'message': 'An internal server error occurred.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

This implementation ensures that:
- **Client errors (400-level)** provide meaningful feedback to the user (e.g., invalid inputs).
- **Server errors (500-level)** respond gracefully with a generic error message and log the actual exception.

---

### **Step 4: Test Error Handling**

1. **Simulate Client Errors:**
   - Send invalid input via the API and ensure the error is correctly caught and returned.
     Example response for an invalid `COUNTY` filter:
     ```json
     {
         "error": "Invalid value provided.",
         "message": "Invalid value provided."
     }
     ```

2. **Simulate Server Errors:**
   - Trigger unexpected exceptions (e.g., database unavailability) and confirm the response is consistent:
     ```json
     {
         "error": "An internal server error occurred.",
         "message": "An internal server error occurred."
     }
     ```

---

### **Step 5: Logging for Better Debugging**

Integrate Django’s logging framework to log errors for debugging. Update `settings.py` with a logging configuration:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

### **Expected Behavior**

1. **Handled Errors:** Specific exceptions return detailed and user-friendly error messages.
2. **Unhandled Errors:** Unexpected exceptions return a standard 500 error response:
   ```json
   {
       "error": "An internal server error occurred.",
       "message": "An unexpected error occurred."
   }
   ```
3. **Log Errors:** Server-side errors are logged to the `errors.log` file.

---

### **Benefits of Robust Error Handling**

1. **Improved Debugging:** Logging ensures all exceptions are traceable.
2. **User Feedback:** Meaningful error responses enhance API usability.
3. **Consistency:** Custom exception handling enforces a standard response format across the application.

---

**24. Asynchronous Tasks with Celery**
---
Celery is a powerful, distributed task queue that allows you to execute tasks asynchronously, enabling better performance for time-consuming operations like sending emails, processing data, or generating reports. Below are the steps to integrate Celery into your Django project.

---

### **Step 1: Install Celery and Redis**

1. Install Celery and Redis:
   ```bash
   pip install celery redis
   ```

2. Ensure Redis is installed and running on your system. Redis acts as the message broker for Celery.

---

### **Step 2: Configure Celery in Django**

1. Add Celery settings in your `stn_project/settings.py`:

   ```python
   CELERY_BROKER_URL = 'redis://redis:6379/0'  # Redis as the message broker
   CELERY_RESULT_BACKEND = 'redis://redis:6379/0'  # Redis to store task results
   CELERY_ACCEPT_CONTENT = ['json']  # Accept only JSON formatted messages
   CELERY_TASK_SERIALIZER = 'json'  # Serialize tasks as JSON
   ```

2. Create a `celery.py` file in your project directory (`stn_project/`):

   ```python
   import os
   from celery import Celery

   # Set the default Django settings module for the Celery program.
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stn_project.settings')

   app = Celery('stn_project')

   # Using a string here means the worker doesn’t have to serialize
   # the configuration object to child processes.
   app.config_from_object('django.conf:settings', namespace='CELERY')

   # Auto-discover tasks from installed apps
   app.autodiscover_tasks()

   @app.task(bind=True)
   def debug_task(self):
       print(f'Request: {self.request!r}')
   ```

3. Update the `__init__.py` file in `stn_project/` to initialize Celery:

   ```python
   from __future__ import absolute_import, unicode_literals

   # This will make sure the app is always imported when
   # Django starts.
   from .celery import app as celery_app

   __all__ = ('celery_app',)
   ```

---

### **Step 3: Create Celery Tasks**

1. In the `journey` app, create a `tasks.py` file to define tasks:

   ```python
   from celery import shared_task
   import time

   @shared_task
   def long_running_task(data):
       """
       Simulates a long-running task.
       """
       time.sleep(10)  # Simulate a task taking 10 seconds
       print(f"Task completed with data: {data}")
       return f"Task completed: {data}"
   ```

---

### **Step 4: Add Redis to Docker Compose**

If you're using Docker, add Redis and a Celery worker service to your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    # Your database configuration

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A stn_project worker -l info
    volumes:
      - .:/app
    depends_on:
      - redis
      - web
```

Start the services with:
```bash
docker-compose up --build
```

---

### **Step 5: Trigger Celery Tasks in Views**

In your views, trigger tasks asynchronously using Celery. Update your view in `journey/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import long_running_task

class TriggerTaskView(APIView):
    """
    API view to trigger a long-running task asynchronously.
    """
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', {})
        try:
            # Trigger the Celery task
            task = long_running_task.delay(data)
            return Response(
                {"message": "Task has been triggered.", "task_id": task.id},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(
                {"error": str(e), "message": "Failed to trigger the task."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

Test the endpoint with a POST request:
```json
POST /api/trigger-task/
{
    "data": "Example data"
}
```

---

### **Step 6: Run Celery Worker**

Start the Celery worker to process tasks:
```bash
celery -A stn_project worker --loglevel=info
```

You should see log entries in the terminal when a task is processed.

---

### **Step 7: Monitor Tasks**

To monitor tasks, consider adding Flower, a Celery monitoring tool. Install Flower:
```bash
pip install flower
```

Add Flower to `docker-compose.yml`:
```yaml
  flower:
    image: mher/flower
    ports:
      - "5555:5555"
    command: celery -A stn_project flower
    depends_on:
      - redis
```

Access Flower at `http://localhost:5555` to view task progress and details.

---

### **Key Benefits of Using Celery**

1. **Asynchronous Processing:** Offloads long-running tasks, improving performance and user experience.
2. **Scalability:** Supports distributed task execution across multiple workers.
3. **Monitoring:** Track tasks in real-time using tools like Flower.
4. **Flexibility:** Handles a variety of tasks, such as email notifications, data imports, and report generation.


---

**24. Caching with Celery Integration**
---
Caching improves the performance of your application by reducing database queries and repetitive computations. When combined with Celery, caching can also store intermediate results of background tasks, ensuring data consistency and optimizing task re-execution.

---

### **Step 1: Install Required Dependencies**

1. Install Django’s caching framework and Celery:
   ```bash
   pip install django-redis celery redis
   ```

2. Ensure that Redis is installed and running as it will serve as both a message broker for Celery and a cache backend.

---

### **Step 2: Configure Caching in Django**

In your `stn_project/settings.py`, configure Redis as the cache backend:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',  # Cache data in Redis database 1
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

### **Step 3: Configure Celery with Caching**

1. Add Celery settings in `settings.py`:

   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the message broker
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Redis to store task results
   CELERY_CACHE_BACKEND = 'default'  # Use the default cache for Celery tasks
   ```

2. Celery will now use the same Redis instance as the cache backend, simplifying data storage and access.

---

### **Step 4: Define a Cached Task in Celery**

In the `journey` app, create a `tasks.py` file with a task that uses caching:

```python
from celery import shared_task
from django.core.cache import cache

@shared_task
def long_running_task(data):
    """
    A long-running task with caching integration.
    """
    cache_key = f"task_cache_{data}"
    # Check if the result is already cached
    if cache.get(cache_key):
        return f"Cached result: {cache.get(cache_key)}"

    # Simulate a long-running computation
    result = f"Processed data: {data}"
    
    # Cache the result with a timeout (e.g., 1 hour)
    cache.set(cache_key, result, timeout=3600)

    return result
```

Here:
- `cache.get(cache_key)` checks if the task result is already cached.
- `cache.set(cache_key, result, timeout=3600)` stores the result in Redis for 1 hour.

---

### **Step 5: Update Views to Trigger Cached Tasks**

Update the `views.py` file to trigger the cached Celery task:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import long_running_task
from django.core.cache import cache

class TriggerCachedTaskView(APIView):
    """
    API view to trigger a cached Celery task.
    """
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', {})
        cache_key = f"task_cache_{data}"
        
        # Check if the result is cached
        if cache.get(cache_key):
            return Response(
                {"message": "Task retrieved from cache.", "result": cache.get(cache_key)},
                status=status.HTTP_200_OK
            )

        # Trigger the Celery task if not in cache
        try:
            task = long_running_task.delay(data)
            return Response(
                {"message": "Task has been triggered.", "task_id": task.id},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(
                {"error": str(e), "message": "Failed to trigger the task."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

This view:
- Checks if the result is cached before triggering the Celery task.
- Responds with the cached result if available, reducing redundant task executions.

---

### **Step 6: Add Redis to Docker Compose**

To integrate Redis for caching and Celery, update `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    # Your database configuration

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A stn_project worker -l info
    volumes:
      - .:/app
    depends_on:
      - redis
      - web
```

Start the services with:
```bash
docker-compose up --build
```

---

### **Step 7: Run and Monitor Celery Tasks**

1. Start the Celery worker:
   ```bash
   celery -A stn_project worker --loglevel=info
   ```

2. Trigger the cached task by sending a POST request to the view:
   ```json
   POST /api/trigger-cached-task/
   {
       "data": "Example data"
   }
   ```

3. Access Redis directly to confirm cached results:
   ```bash
   redis-cli
   keys *
   ```

---

### **Optional: Add a Monitoring Tool for Celery**

To track tasks and cache performance:
1. Install Flower for Celery:
   ```bash
   pip install flower
   ```

2. Add Flower to `docker-compose.yml`:
   ```yaml
   flower:
     image: mher/flower
     ports:
       - "5555:5555"
     command: celery -A stn_project flower
     depends_on:
       - redis
   ```

3. Access Flower at `http://localhost:5555`.

---

### **Key Benefits**

1. **Improved Performance:**
   - Cached results reduce redundant Celery task execution and database queries.
2. **Enhanced Scalability:**
   - Redis handles both task messaging and caching efficiently.
3. **Consistency:**
   - Combines Celery’s asynchronous capabilities with Django’s robust caching framework.
4. **Reduced Latency:**
   - Frequent results are retrieved from cache without re-executing the task.

---

**25. Logging in Django**
---
Logging allows you to capture critical events and errors during the execution of your application. It is crucial for debugging, monitoring, and providing transparency for operations in both Django views and tasks. Follow the steps below to set up and utilize logging effectively.

---

### **Step 1: Configure Logging in Django**

Django uses Python’s built-in `logging` module to manage logs. Add the following `LOGGING` configuration in `stn_project/settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django_errors.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

#### Key Features of the Configuration:
1. **Handlers:** Specify where logs will be written (e.g., `console` for terminal logs, `file` for logs saved to `django_errors.log`).
2. **Formatters:** Define log message formats (e.g., verbose format includes timestamps and modules).
3. **Loggers:** Set logging levels (`INFO`, `WARNING`, `ERROR`, etc.) for the Django application.

---

### **Step 2: Use Logging in Views**

Implement logging in your views to capture actions and exceptions. For example, in `journey/views.py`:

```python
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Initialize the logger
logger = logging.getLogger(__name__)

class ExampleView(APIView):
    """
    A sample API view with logging integration.
    """
    def get(self, request, *args, **kwargs):
        logger.info("GET request received in ExampleView.")
        try:
            # Perform logic
            logger.info("Processing request successfully.")
            return Response({"message": "Request successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
```

#### Benefits:
- Logs provide detailed feedback on user requests and application errors.
- Easily track and debug issues by inspecting logged events.

---

### **Step 3: Integrate Logging in Celery Tasks**

Celery uses Python’s logging module by default, but you can customize task-level logging for better visibility.

In `journey/tasks.py`:

```python
import logging
from celery import shared_task

# Initialize the logger for Celery tasks
logger = logging.getLogger('celery')

@shared_task
def sample_task(data):
    """
    A sample Celery task with logging integration.
    """
    logger.info(f"Task started with data: {data}")
    try:
        # Simulate processing
        result = f"Processed data: {data}"
        logger.info(f"Task completed successfully with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Task failed with error: {str(e)}")
        raise
```

#### Features:
- Logs provide detailed feedback during task execution.
- Errors and exceptions in tasks are captured and logged for further investigation.

---

### **Step 4: Add Redis and Celery Worker to Docker Compose**

For task execution and logging, update your `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A stn_project worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
```

Start the services:
```bash
docker-compose up --build
```

---

### **Step 5: View Logs**

1. **Console Logs:** View logs in the terminal when running the Django server (`python manage.py runserver`) or Celery worker (`celery -A stn_project worker --loglevel=info`).
2. **Log File:** Open `django_errors.log` to inspect ERROR-level logs.
3. **Real-Time Monitoring:** Use Flower (optional) for Celery task monitoring:
   ```bash
   pip install flower
   celery -A stn_project flower
   ```
   Access Flower at `http://localhost:5555`.

---

### **Expected Logs**

1. **Sample Console Log:**
   ```
   INFO GET request received in ExampleView.
   INFO Processing request successfully.
   ERROR An error occurred: Division by zero
   ```

2. **Sample Task Log (Celery Worker):**
   ```
   [2023-03-25 14:23:10,123: INFO] Task started with data: {"example": "data"}
   [2023-03-25 14:23:20,456: INFO] Task completed successfully with result: Processed data
   [2023-03-25 14:24:30,789: ERROR] Task failed with error: Unable to connect to Redis
   ```

---

### **Key Benefits of Integrated Logging**

1. **Centralized Monitoring:**
   - Captures logs from both Django views and Celery tasks.
   - Tracks errors across synchronous and asynchronous processes.

2. **Error Debugging:**
   - Logs help identify the root cause of issues, whether in HTTP requests or task executions.

3. **Scalability:**
   - Redis and Celery workers ensure robust task execution, while logs provide visibility into their performance.

---

**26. CI/CD (Example with GitHub Actions)**
---
* Create a `.github/workflows/deploy.yml` file:

```yaml
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and run docker-compose
        run: docker-compose up --build -d
```


**27. Health Checks**
---
* Create a health check endpoint in `journey/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})
```

* Add it to `journey/urls.py`.

**28. Freeze Requirements**:
---
   - Generate or update your `requirements.txt` file with all installed packages. Run:
     ```bash
     pip freeze > requirements.txt
     ```


This comprehensive guide should provide a solid foundation for your "stn_backend" project. Remember to adapt the code and configurations to your specific needs and requirements.
