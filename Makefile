make_migr:
	python manage.py makemigrations movie
migr:
	python manage.py migrate
test:
	python manage.py test
super:
	python manage.py createsuperuser
shell:
	python manage.py shell