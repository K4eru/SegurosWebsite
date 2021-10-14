@python -m venv venv
@Call ".\venv\Scripts\activate.bat"
@Call pip install -r requirements.txt
@python manage.py makemigrations
@python manage.py migrate
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin') | python manage.py shell
@python manage.py runserver 8001