###Requirement
The project requires WebOb==1.8.5 package and WSGI server installed (gunicorn for example).<br>

### uWSGI framework <br>
##### Usage and requirements
First U must run your server.<br>
Example shows gunicorn activation:<br>
In folder with app.py u have to call gunicorn with framework file ([src/uwsgi/app.py](/src/uwsgi/app.py)), main class('app') and hostname with port in its arguments.<br>
Then call file [src/uwsgi/app.py](/src/uwsgi/app.py)
Example of use:<br>
```
>>>pip install webob
>>>pip install gunicorn
>>>cd /path/to/uwsgi/app.py
>>>gunicorn app:app -b localhost:80
>>>python /path/to/uwsgi/app.py
```
After successfully launching your server, u will see something like this in your console:<br>
![result](https://github.com/aozerets/web-dev/tree/master/share/images/running.jpg)<br>
Now u are able to see demo pages in browser by typing hostname:port and path.<br>
Paths u are interested in are located in the same file [src/uwsgi/app.py](/src/uwsgi/app.py).<br>
For demo purpose in project added 3 demo paths: "/", "/home", "detail/<name>/<age>".<br>
U can add the ones u need just adding a new function with app.route("/your route") decorator.<br>


