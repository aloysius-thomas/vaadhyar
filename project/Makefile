
.PHONY: install
install:
	pip install -r requirement.txt

.PHONY: migrations
migrations:
	 python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: superuser
superuser:
	 python manage.py createsuperuser

.PHONY: update
update: install migrations migrate run;


PORT ?= 8000

.PHONY: run
run:
	python manage.py runserver $(PORT)

