#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("izracun.html")

    def post(self):
        st_1 = self.request.get("st_1")
        st_2 = self.request.get("st_2")
        operacija = self.request.get("operacija")
     
        if operacija == "deljenje":
            rezultat = float(st_1) / float(st_2)
             
        elif operacija == "mnozenje":
            rezultat = int(st_1) * int(st_2)
                     
        elif operacija == "sestevanje":
            rezultat = int(st_1) + int(st_2)
                             
        elif operacija == "odstevanje":
            rezultat = int(st_1) - int(st_2)

        view_vars = {
            'st_1': st_1,
            'st_2': st_2,
            'operacija': operacija,
            'rezultat': rezultat,
            }
        return self.render_template("rezultat.html", view_vars)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', MainHandler),
], debug=True)