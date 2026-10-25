# sticky notes

a small django app for jotting down sticky notes (gaming to-dos, backlog, raid times, whatever). built as part of the hyperiondev bootcamp.

## features

- create, view, edit, delete notes (CRUD)
- gaming-themed dark neon UI
- django admin for managing notes
- unit tests for models, forms and views

## setup

```sh
python -m venv venv
source venv/bin/activate   # on windows: venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

then open http://127.0.0.1:8000/

## run the tests

```sh
python manage.py test notes
```

## admin

```sh
python manage.py createsuperuser
```

then log in at http://127.0.0.1:8000/admin/

## layout

- `notes/` - the app (models, views, forms, urls, templates, tests, css)
- `sticky_notes/` - project settings and root urls
- `diagrams/` - use case, sequence and class diagrams (svg)
