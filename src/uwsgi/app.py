#! /usr/bin/env python3

import my_uwsgi

app = my_uwsgi.API()


@app.route("/")
def demo(request, response):
    user_agent = request.environ.get("HTTP_USER_AGENT", "No User Agent Found")
    response.text = "<h1>Hi there! It is the DEMO page.</h1><br>"
    response.text += "<h2>Hello, World!</h2><br>"
    response.text += "Glad to meet you, my friend from browser:<br> %s<br>" % user_agent


@app.route("/home")
def home(request, response):
    response.text = "Welcome! It is the MAIN page."


@app.route("/detail/<name>/<age>")
def detail(request, response, name, age):
    response.text = "Greetings! This is the page of DETAIL information!"
    response.text += "<h2>Your name is: %s</h2><br><h2>And your are %s years old!!</h2>" % (name, age)
