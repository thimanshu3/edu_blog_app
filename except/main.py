import os
import json
import datetime
import psycopg2
import psycopg2.extras
import tornado.httpserver
import tornado.ioloop
import tornado.web
from flaskext.mysql import MySQL
import pymysql.cursors



class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index1.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        created = datetime.datetime.now()
        connection = pymysql.connect(host='localhost',user='root',password='rj27CA@1783',db='pythonlogin',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cur=connection.cursor()
        cur.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
        account = cur.fetchone()
        if account:

            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            self.render("register.html")
        else:
            msg='404'
        return self.render("contact.html")

class registerHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('register.html')

class forgotHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('forgot.html')

class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render("404.html")
        else:
            self.render("error.html")

class My404Handler(BaseHandler):
    def prepare(self):
        raise tornado.web.HTTPError(404)

class MyCustomHandler(BaseHandler):
    def get(self):
        if not self.valid_arguments():
            raise tornado.web.HTTPError(400)


class AboutHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('about.html')


class ContactHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('contact.html')


    def post(self):
        self.write('Submitted successfully')




def main():

    settings = dict(
        cookie_secret=str(os.urandom(45)),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        autoreload=True,
        gzip=True,
        debug=True,
        login_url='/login',
        autoescape=None
    )

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/contact", ContactHandler),
        (r"/register", registerHandler),
        (r"/forgot", forgotHandler)
    ], **settings, default_handler_class=My404Handler)

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
