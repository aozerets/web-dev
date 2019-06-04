### Requirement
The project requires Django==2.2.1 and django-debug-toolbar==1.11 package installed.<br>
U can use [requirements.txt](/src/django_app/requirements.txt) for easy install.<br>
```
>>>pip install -r requirements.txt
```
### Django App <br>
##### Usage and requirements
To run App u must go to folder ".../src/django_app" and execute the following commands:.<br>
```
/path/to/src/django_app>>>python manage.py makemigrations
/path/to/src/django_app>>>python manage.py migrate
/path/to/src/django_app>>>python manage.py createsuperuser
/path/to/src/django_app>>>python manage.py runserver
```
After successfully launching your app, u will see something like this in your console:<br>
![running](https://github.com/aozerets/web-dev/blob/master/share/images/django_init.jpg)<br>
Now U are able to see demo pages in browser by typing hostname:port(localhost:8080) and path or moving by links on pages.<br>
U can move to "/admin" page and add some staff to the shop (login and password are your superuser credentials).<br>
There are 6 paths: "/sales/", "/sales/<`name`>/", "/sales/products/", "/sales/products/<`int:prod_id`>/", "/sales/orders/", "/sales/orders/<`int:ord_id`>/" in project for use.<br>
