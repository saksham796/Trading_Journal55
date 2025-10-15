Trading Journal (Django, client-side storage only)

Overview
- Secure trading journal built with Django for authentication and pages.
- Per your requirement, no trade data is stored on the server or in any database. All trade entries are saved only on the user's device using the browser's localStorage.
- The unlock step gates visibility of your trades during the session. No passwords or trade content are persisted on the server.

Requirements
- Python 3.13+
- Django 5.2+
- No database setup required for trades. Django's default DB is still used for user accounts only.

Setup
1) Install dependencies
   - Using uv or pip based on pyproject:
     uv pip install -r uv.lock  (if you maintain a lock)
     or
     uv pip sync
     or
     pip install -e .

2) Initialize Django (users/auth only)
   cd Trading_Journal
   python manage.py migrate
   python manage.py createsuperuser

3) Run server
   python manage.py runserver

Usage
- Navigate to http://127.0.0.1:8000/
- Log in or sign up, then go to /journal/unlock and enter your unlock password for the session.
- Add trades at /journal/add. Trades are stored locally on your browser/device and rendered on /journal/dashboard.

Deploying to Railway
- Prereqs: Railway account and CLI or use the Dashboard. This project includes a Procfile for the web process and uses Gunicorn.
- Environment variables (recommended):
  - SECRET_KEY: set a strong secret for production
  - DJANGO_DEBUG: set to false
  - ALLOWED_HOSTS: your Railway domain(s), e.g. yourapp.up.railway.app (comma-separated for multiple)
  - CSRF_TRUSTED_ORIGINS: e.g. https://yourapp.up.railway.app
- Static files: WhiteNoise is enabled in production; Railway will serve files collected into ./Trading_Journal/staticfiles. On first deploy, run:
  - railway shell → python Trading_Journal/manage.py collectstatic --noinput
- Database: Trades are stored only on the client (localStorage). Django’s DB is used only for auth/sessions. Railway ephemeral disk resets on redeploy; for persistent users, attach Railway Postgres and set DATABASES accordingly (not configured by default in this repo). Otherwise, recreate users after deploy by running migrations and createsuperuser as below.
- Migrations and superuser:
  - railway shell → python Trading_Journal/manage.py migrate
  - railway shell → python Trading_Journal/manage.py createsuperuser
- Start command: Procfile defines
  - web: gunicorn Trading_Journal.wsgi:application --bind 0.0.0.0:$PORT
- After deploy: visit your Railway URL, sign up or log in, unlock, add trades.

Notes on storage and privacy
- Trades never leave your device and are not stored in any server database.
- Clearing your browser data (site data/localStorage), switching browsers, devices, or profiles will remove or not show your trades.
- To move data between devices, you would need an export/import feature (not included by default).

Security Notes
- The unlock password is used to gate visibility only in this build. It is kept in the server-side session for the duration of your login and cleared on logout.
- Since data is local-only, ensure your device/browser is secure. Consider using OS-level disk encryption.

Configuration
- No trade database configuration is necessary. Templates are loaded from app templates and the project template directory is configured.

Limitations
- Trades are tied to the specific browser and device via localStorage.
- Clearing browser storage deletes your saved trades.




Troubleshooting
- If you see an error like: "no such table: auth_user" when logging in or signing up, it means Django auth tables haven’t been created yet.
- Fix:
  1) cd Trading_Journal
  2) python manage.py migrate
  3) Restart the server and try again.
- The app now shows a friendly message instead of a server error until migrations are applied.
