* **Install PostgreSQL**:
   - Ensure PostgreSQL is installed on your system. The `pg_config` executable is part of the PostgreSQL installation.
   * **Linux:**
        * Install PostgreSQL, as it includes the `pg_config` executable required for building `psycopg2` from source. On Linux, use your package manager 
        ```bash
        sudo apt install postgresql
        ```
        * Make sure the directory containing `pg_config` (typically `/usr/bin`)
        
   * **Windows:**
        * For Windows, you can download PostgreSQL from the [official site](https://www.postgresql.org/download/) and ensure you add PostgreSQL's `bin` directory to your system's PATH during installation.

        * **Add `pg_config` to Windows PATH**:
        - If PostgreSQL is installed but `pg_config` is not found, you need to add the directory containing `pg_config` (usually `<PostgreSQL_Installation_Directory>\bin`) to your system's PATH environment variable.
        - For example. `C:\Program Files\PostgreSQL\17\bin` 

        **Steps to Add to Windows PATH**:
        - Open "Environment Variables" in your system settings.
        - Find the `Path` variable under "System variables."
        - Click "Edit" and add the path to the `bin` directory of your PostgreSQL installation.

* **Install or Update the Windows SDK and UCRT Headers**:
   - Download the latest [Windows SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/) and install it.
   - During installation, ensure the **Universal C Runtime (UCRT)** is selected under "Installation Options."

* **Update Visual Studio Build Tools**:
   - If you're using Visual Studio 14.0 (2015), it may not fully support your system configuration.
   - Download and install the latest [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and select the "Desktop Development with C++" workload during installation.

    * **Add Correct Paths to Environment Variables**:
    - Verify that the paths to your `cl.exe`, Windows SDK, and UCRT headers are correctly added to your `PATH` environment variable.
        For example:
        ```bash
        SET PATH=C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\x86_amd64;%PATH%
        SET PATH=C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\ucrt;%PATH%
        ```
        **Steps to Add to Windows PATH**:
        - Open "Environment Variables" in your system settings.
        - Find the `Path` variable under "System variables."
        - Click "Edit" and add the path to the `bin` directory of your Visual Studio installation.

* **Verify Installation**:
   - After installation, the UCRT headers should be located in a directory like:
     ```
     C:\Program Files (x86)\Windows Kits\10\Include\<SDK-Version>\ucrt
     ```
     Replace `<SDK-Version>` with the version number of the SDK you installed.


**Creating the Django App Admin and Superuser**

You need to run Django's migrations to create the database tables. Here's how to do it:

1.  **Ensure you are in the `web` container:**

    ```bash
    docker-compose exec web bash
    ```

2.  **Run the migrations:**

    ```bash
    python manage.py migrate
    ```

    This command will apply all pending migrations, creating the necessary database tables.

3.  **Then, run createsuperuser:**

    ```bash
    python manage.py createsuperuser
    ```

    After running migrate, the auth_user table will exist, and this command will work.

**Explanation**

* Django's migrations are used to create, modify, and delete database tables.
* The `auth` app (Django's authentication system) has migrations that create the `auth_user` table, which is required for creating superusers.
* By running `python manage.py migrate`, you are applying these migrations and creating the `auth_user` table.

**Important Considerations**

* **Docker Compose Up:** Ensure that your Docker containers are running (`docker-compose up`).
* **Database connection:** If the migrate command still has issues, double check that your database container is running properly, and that the settings.py file is configured correctly.
* **order of operations:** It is extremely important that the migrate command is run before the createsuperuser command.

