# research answers

## 1. how HTTP applications preserve state across request-response cycles

HTTP is stateless, so every request a browser sends is treated as if the server
has never seen that user before. That is obviously a problem for anything that
needs to remember a user between pages, like staying logged in or keeping items
in a shopping cart. The usual fix is a combination of cookies and server-side
sessions. The first time a user hits the site, the server creates a session, gives
it a unique ID, and sends that ID back in a `Set-Cookie` header. The browser
then attaches that cookie to every later request, which lets the server look up
the matching session data and know who the user is.

For login specifically, the user submits a username and password through a form.
The server checks the credentials, and if they pass, it links the current session
to that user's account. From then on, as long as the session cookie is valid, the
user stays logged in without re-entering their password. Django handles most of
this out of the box with its session middleware, which creates and tracks
sessions in the database by default. On top of that, CSRF tokens, HTTPS, and
flags like HttpOnly and Secure on the cookie help stop attackers from stealing
or forging sessions.

## 2. Django database migrations to a server-based database like MariaDB

By default a Django project runs on SQLite, which is a single file on disk. To
move the project onto a server-based database like MariaDB, you only need to
change a few settings and reinstall. First, install a driver that Django can talk
to MariaDB with. `mysqlclient` is the common one, and it goes in with
`pip install mysqlclient`. On the MariaDB side you need a database and a user
with permission on that database.

Next, open `settings.py` and change the `DATABASES` dictionary so `ENGINE` is
`django.db.backends.mysql` and `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT`
all point at the MariaDB server. Once the connection details are right, run
`python manage.py makemigrations` to catch any pending model changes, then
`python manage.py migrate` to actually build the tables in MariaDB. Django reads
the migration files and creates everything for you.

If there is existing data in the old SQLite file that needs to come across, you
can dump it with `python manage.py dumpdata > data.json` and load it with
`loaddata` after migrating. It is also a good idea to keep the database password
out of `settings.py` by reading it from an environment variable, and to back the
database up before running migrations.
