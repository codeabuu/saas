# Django SaaS Project

This project builds the foundations for a Software as a Service business by leveraging Django, Stripe for payments, Tailwind, htmx, Neon Postgres, Redis, and more.

The goal of this project is to create a reusable foundation for building SaaS products for your business or startup.

## References

- Deploy DJango on [Railway](https://railway.app/?referralCode=fgkUis) with this [Dockerfile and guide](https://www.codingforentrepreneurs.com/blog/deploy-django-on-railway-with-this-dockerfile)
- Use a serverless postgress with [Neon](https://neon.tech/) 


## Getting Started
### Clone
```bash
git clone https://github.com/codeabuu/saas
```
### Create a Virtual Environment
*mac0S/Linux*
```bash
python3 --version # should be 3.11 or higher
python3 -m venv venv
source venv/bin/activate
```

*Windows*
```bash
c:\Python312\python.exe -m venv venv
.\venv\Scripts\activate
```
### Install Requirements
```bash
# with venv activated
pip install pip --upgrade && pip install -r requirements.txt
```
### Sample dotenev to dotnev
```bash
cp .env.sample .env
cat .env
```
Values Include:
- DJANGO_DEBUG=1
- DJANGO_SECRET_KEY=""
- DATABASE_URL=""
- EMAIL_HOST="smtp.gmail.com"
- EMAIL_PORT="587"
- EMAIL_USE_TLS=True
- EMAIL_USE_SSL=False
- EMAIL_HOST_USER=""
- EMAIL_HOST_PASSWORD=""
- ADMIN_USER_EMAIL=""
- STRIPE_SECRET_KEY=""

### Create DDJANGO_SECRET_KEY
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
or
```bash
openssl rand -base64 64
```
or
```bash
python -c 'import secrets; print(secrets.token_urlsafe(64))'
```
Once you have this value, add update DJANGO_SECRET_KEY in .env .

### Create [Neon](https://neon.tech/) Postgress Database
**Install Neon CLI**
Using the Neone CLI via homebrew:
```bash
brew install neonctl
```

**Login to Neon CLI**
```bash
neonctl auth
```
This will open a browser window to login

**Create a new Neon project (optional)**
```bash
neonctl projects create --name saas
```

**Get the project ID**
Once created, get the project ID:
```bash
neonctl projects list
```
Projects
```bash
┌──────────────────────────┬────────────────────────────┬───────────────┬──────────────────────┐
│ Id                       │ Name                       │ Region Id     │ Created At           │
├──────────────────────────┼────────────────────────────┼───────────────┼──────────────────────┤
│ steep-base-11409687      │ saas                       │ aws-us-east-2 │ 2024-11-02T04:03:07Z │
└──────────────────────────┴────────────────────────────┴───────────────┴──────────────────────┘
```
```bash
PROJECT_ID=steep-base-11409687
```
Replace steep-base-11409687 with your project id.

**Get Database connection string**
```bash
neonctl connection-string --project-id "$PROJECT_ID"
```

### Run Migrations
```bash
source venv/bin/activate 
# or .\venv\Scripts\activate if windows
cd src
python manage.py migrate
```
### Create a Superuser
```bash
python manage.py createsuperuser
```

### Pull Vendor static files
```bash
python manage.py vendor_pull
```

### Creating Stripe Account