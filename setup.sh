#!/bin/bash
rm -fr .vscode
rm -fr ENV_DIR
rm -fr factories
rm db.sqlite3 db.sqlite3.old geckodriver.log requirements-dev.txt TODO
rm minhoteca/settings.py
mv minhoteca/settings.py.prd minhoteca/settings.py
rm minhoteca/.env
mv minhoteca/.env.prd minhoteca/.env
python ./createdb.py
python manage.py makemigrations
python manage.py migrate
python manage.py compilescss
python manage.py collectstatic --no-input
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(email='minhoteca@livrosviajantes.com.br', password='S3nh@root')" | python manage.py shell;

# gunicorn --bind 0.0.0.0:80 --workers 3 minhoteca.wsgi:application --log-level info

python manage.py runserver 0.0.0.0:80

exec "$@"
