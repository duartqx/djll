# DJLL

![djll](https://github.com/duartqx/images/blob/main/djll.png?raw=true "djll")

DJLL is a simple system with user CRUD and authentication using Django, DRF, Fernet (cryptography.fernet (py) / fernet.js) and HTMX.

The primary purpose of writing this small system was to learn HTMX, but I also needed a JSON RESTful API due to a constraint. Looking back, I think I should've written instead using alpine.js instead of HTMX, it would probably make my life easier when working with json. 
HTMX is a great tool to work with, although the documentation is a little sparse and the community is not large enough. The only downside is that it can be a bit of a hassle to work with JSON in conjunction with it, and if these two things improve, it will explode in popularity.

## What could improve:

DJLL is a small SPA with login, logout, user creation, deletion, and update capabilities thanks to HTMX, but it has one flaw: A full page reload loses context and the user is sent back to the index page. This is not a major issue for now, as it was my first attempt with HTMX.

## How to:

To test the system, you can perform all of the typical actions that you would do when running a local Django application:

```bash
git clone https://github.com/duartqx/djll.git
cd djll
python -m venv .venv
source .venv/bin/activate
pip install -r requirements
python manage.py migrate
python manage.py runserver
``` 
