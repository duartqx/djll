# DJLL

![djll](https://github.com/duartqx/images/blob/main/djll.png?raw=true "djll")

DJLL is a simple system with user CRUD and authentication using Django, DRF, Fernet (cryptography.fernet (py) / fernet.js) and HTMX.

The primary purpose of writing this small system was to learn HTMX, but I also needed a JSON RESTful API due to a constraint. Looking back, I think I should've written instead using alpine.js instead of HTMX, it would make my life easier when working with json. 
HTMX is a great tool to work with, although the documentation is a little sparse and the community is still growing. The only downside is that it can be a bit of a hassle to work with JSON in conjunction with it, and if these two things improve, it will explode in popularity.

## How to:

To test the system, you can perform all of the typical actions that you would do when running a local Django application:

```bash
git clone https://github.com/duartqx/djll.git
cd djll
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
``` 

## UPDATE

The templates have been restructured, and custom JavaScript functions previously handling JSON responses have been removed. Instead, I’ve added Django views which inherit from the api views and handle all Htmx requests, including receiving JSON data and responding with rendered HTML templates. This modification has led to a significant simplification of the templates, enabling Htmx to solely manage page interactivity. Upon examining the core/templates, you’ll notice that all components are simple HTML, with declarative Htmx tags

## Demo

https://github.com/duartqx/djll/assets/49421452/262b66a7-3910-49f1-bb42-e4a1513d2dba




