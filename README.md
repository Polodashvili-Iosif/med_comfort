# med_comfort

![Workflow Status](https://github.com/Polodashvili-Iosif/med_comfort/actions/workflows/main.yml/badge.svg)
[![Codecov](https://codecov.io/github/Polodashvili-Iosif/med_comfort/graph/badge.svg)](https://codecov.io/github/Polodashvili-Iosif/med_comfort)

The website of the medical clinic "Med Comfort". 

## Site:

https://medcomfort.site

### Instalation:

Cloning the repository:

```
git clone https://github.com/maximkidalov/foodgram-project-react.git
```

Create the file `infra/.env` using the example:
```
SECRET_KEY='<your-secret-key>'
DEBUG=False
ALLOWED_HOSTS=<your-server-address>,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://<your-server-address>
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-email-app-password>
POSTGRES_USER=user
POSTGRES_PASSWORD=tpassword
POSTGRES_DB=postgres_db
DB_HOST=db
DB_PORT=<port>
```

Launching Docker in the `infra/` directory:

```
docker-compose up -d
```

Run migrations, collect statics, upload data, and create an administrator:
```
docker compose -f docker-compose.yml exec backend python manage.py migrate
docker compose -f docker-compose.yml exec backend python manage.py collectstatic --no-input 
docker-compose.yml exec backend cp -r /app/staticfiles/. /backend_static/
docker-compose.yml exec backend python manage.py loaddata clinics_data.json
docker-compose.yml exec backend python manage.py loaddata services_data.json
docker-compose.yml exec backend python manage.py loaddata users_data.json
docker-compose.yml exec backend python manage.py loaddata doctors_data.json
docker-compose exec backend python manage.py createsuperuser
```

### Description:

The application is an online service that allows users to:
- Register and log in to your profile
- View the services provided, clinics and doctors, and appointment appointments
- Make an appointment with a doctor