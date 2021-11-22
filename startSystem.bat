@python -m venv venv
@Call ".\venv\Scripts\activate.bat"
@Call pip install -r requirements.txt
@python manage.py makemigrations
@python manage.py migrate
echo from django.contrib.auth import get_user_model; from systemAuth.models import company, commonUserModel; User = get_user_model(); adminUser = User.objects.create_superuser('admin', 'admin@admin.com', 'admin'); com = company(name='Test1', description='Test1', responsable=1, userAddress='Test1'); com.save(); commonUser = commonUserModel(user = adminUser, firstName = 'admin', lastName = 'admin', phoneNumber = 123456789, rut = 123456789, userType = 2, company = com); commonUser.save() | python manage.py shell
@python manage.py runserver 8000