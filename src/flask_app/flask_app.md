### Requirement
The project requires Flask==1.0.3 package installed.<br>
```
>>>pip install flask
```

### Flask App <br>
##### Usage and requirements
First go to [/path/to/src/flask_app/config.py](/src/flask_app/config.py) and change the host and port in SERVER_NAME in DevelopmentConfig class.<br>
After that U can run your app on chosen host.<br>
Go to the folder in which the project was installed, and call the main file[main](/src/flask_app/main.py).<br>
Example of use:<br>
```
/path/to/flask_app >>> ./main.py
```
After successfully launching your app, u will see something like this in your console:<br>
![result](https://github.com/aozerets/web-dev/blob/master/share/images/flask_init.jpg)<br>
Now U are able to see demo pages in browser by typing hostname:port and path or moving by links on pages.<br>
There are 4 paths: "/", "/<`name`>/", "/products/", "/products/<`int:prod_id`>/" in project for use.<br>
