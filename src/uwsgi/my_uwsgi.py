#! /usr/bin/env python3

from webob import Request, Response
from itertools import zip_longest
from subprocess import PIPE, Popen
from configparser import ConfigParser


class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = self.parse_args(path, request_path)
            if path == request_path:
                return handler, {}
            elif parse_result and all([x for x in parse_result.values()]):
                return handler, parse_result
        return None, None

    @staticmethod
    def parse_args(pattern, resource):
        keys = {idx: x.replace("<", "").replace(">", "") for idx, x in enumerate(pattern.split("/")) if "<" in x and ">" in x}
        values = [x for idx, x in enumerate(resource.split("/")) if idx in keys.keys()]
        return dict(zip_longest(keys.values(), values))

    @staticmethod
    def default_response(response):
        response.status_code = 404
        response.text = "<h1>Not found.</h1><br><h1>COME BACK LATER!</h1>"
    #
    # @staticmethod
    # def _exec(cmd):
    #     """Executes the received command in shell,
    #        automatically decodes input to UTF-8
    #        and removes unnecessary symbols from the end of str.
    #        :cmd  -> string."""
    #
    #     proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    #     out = proc.communicate(timeout=60)[0]
    #     return out.decode(errors="replace").strip(" \n\t")
    #
    # def run(self, file, app):
    #     conf = ConfigParser()
    #     conf.read('conf.ini')
    #     host = conf.get('host', 'ip') + ":" + conf.get('host', 'port')
    #     self._exec("gunicorn %s:%s -b %s" % (file.split(".")[0], app, host))
