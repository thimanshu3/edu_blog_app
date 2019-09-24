import tornado.ioloop
import tornado.web
import os
import tornado.httpserver
import tornado.options
from tornado.options import define, options
import tormysql
from tornado import gen
import random
import string
import bcrypt
import asyncio
import json
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor
from ast import literal_eval as make_tuple


define("port", default=5000, help="run on the given port", type=int)

# defining db credentials
pool = tormysql.helpers.ConnectionPool(
    max_connections = 20, #max open connections
    idle_seconds = 7200, #conntion idle timeout time, 0 is not timeout
    wait_connection_timeout = 3, #wait connection timeout
    host = "localhost",
    user = "root",
    passwd = "rj27CA@1783",
    db = "edu_db",
    charset = "utf8"
)

# class for handling 404 status

class My404Handler(tornado.web.RequestHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def prepare(self):
        self.set_status(404)
        self.render("404.html")

# base handler class
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# class for forgot 
class ForgotHandler(BaseHandler):
    def get(self):
        self.render('forgot.html')

# main class
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        email =self.get_secure_cookie("user")
        entry1 = yield pool.execute("SELECT * FROM blog_user")
        entry2 = yield pool.execute("SELECT * FROM blog_user order by blog_likes desc limit 5")
        entry3 = yield pool.execute("SELECT blog_id FROM blog_likes where blog_like = '"+email.decode('ASCII')+"'")
        entry4 = yield pool.execute("SELECT blog_id FROM blog_likes where blog_dislike = '"+email.decode('ASCII')+"'")
        data1=entry1.fetchall()
        data2=entry2.fetchall()
        
        if entry3.rowcount or entry4.rowcount:
            print("chale gaye bhai")
            data3 = entry3.fetchall()
            data4 = entry4.fetchall()    
            data=[data1,data2,data3,data4]
            self.render("home.html", entries=data)

        else:
            data=[data1,data2]
            self.render("home.html", entries=data)

        # allblogs = yield pool.execute("Select * from blog_user")
        # trending = yield pool.execute("select * from blog_user order by blog_likes desc limit 5")
        # entries = [allblogs , trending]
        # self.render("home.html", entries=entries)

# login activity calss
class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 20:
            return
        msg = ''
        self.render('index1.html',msg = msg)

    @tornado.gen.coroutine
    def post(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 20:
            return
        getuseremail = tornado.escape.xhtml_escape(self.get_argument("email"))
        getpassword = tornado.escape.xhtml_escape(self.get_argument("password"))
        getpassword = getpassword.encode('utf-8')
        pass1 = hashlib.sha1(getpassword).digest()
        pass2 = hashlib.sha1(pass1).hexdigest()
        pass2 = "*" + pass2.upper()
        cursor = yield pool.execute("Select * from users_details where user_emai='"+getuseremail+"' and user_password='"+pass2+"'")
        rc=cursor.rowcount
        cursor.close()
        if(rc==0):
            print("no such user exist")
            incorrect = self.get_secure_cookie("incorrect") or 0
            increased = str(int(incorrect)+1)
            self.set_secure_cookie("incorrect", increased)
            msg = "404"
            # self.set_flash('Error Login incorrect')
            self.render("index1.html",msg=msg)
        else:
            data = cursor.fetchall()
            self.set_secure_cookie("user", self.get_argument("email"))
            self.set_secure_cookie("incorrect", "0")
            self.redirect("/home")
           

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", self.reverse_url("main")))

class ProfileHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        useremail = str(self.get_secure_cookie("user"))
        useremail = useremail.strip('b')
        getuseremail = useremail.strip('"+useremail+"')
        userdetails = yield pool.execute("Select * from users_details where user_emai="+getuseremail+"")
        userpost = yield pool.execute("Select * from blog_user where user_email="+getuseremail+"")
        userdetails.close()
        userpost.close()
        userdetails = userdetails.fetchall()
        userpost = userpost.fetchall()
        msg = [ userdetails ,userpost ]
        print(msg[0][0][0])
        
        
        self.render("profile.html" , msg = msg  )

class StoreLikeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        # getid = tornado.escape.xhtml_escape(self.get_argument("storelike"))
        blogid = self.request.arguments
        feedbackid = ''.join(random.choice(string.ascii_letters) for i in range(10))
        blog_like = self.get_secure_cookie("user")
        blog_like = blog_like.decode('ASCII')

        for key, value in blogid.items():
            blogid = key 
        
        cursor = yield pool.execute("INSERT INTO `blog_likes` (`blog_like`, `blog_id`, `action_id`) VALUES ('"+blog_like+"', '"+blogid+"','"+feedbackid+"');")
        cursor.close()
        cursor = yield pool.execute("SELECT blog_likes from blog_user WHERE blog_id= '"+blogid+"';")
        like_count = cursor.fetchall()
        cnt = 0
        cursor.close()
        if like_count[0][0] is None:
            cnt=1
            cursor = yield pool.execute("UPDATE blog_user SET blog_likes=1 WHERE blog_id= '"+blogid+"';")
        else:
            cnt=like_count[0][0]+1
            cursor = yield pool.execute("UPDATE blog_user SET blog_likes=blog_likes+1 WHERE blog_id= '"+blogid+"';")
        self.xsrf_token 
        cursor.close()
        self.write({"status": "ok", "sent": blogid, "cnt":cnt}) 
        self.finish()

class DeleteLikeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        delete_like = self.get_secure_cookie("user")
        delete_like = delete_like.decode('ASCII')
        for key, values in blogid.items():
            blogid = key
        # useful code goes here
        cursor = yield pool.execute("UPDATE blog_user SET blog_likes=blog_likes-1 WHERE blog_id= '"+blogid+"';")
        cursor.close()
        cursor = yield pool.execute("SELECT blog_likes from blog_user WHERE blog_id= '"+blogid+"';")
        like_count = cursor.fetchall()
        cursor = yield pool.execute("DELETE FROM blog_likes WHERE blog_id = '"+blogid+"' and blog_like = '"+delete_like+"'")
        cursor.close()
        self.xsrf_token
        self.write(json.dumps({"status": "ok", "sent": blogid,"cnt":like_count[0][0]}))

        self.finish()
        
        
class StoreDisLikeHandler(tornado.web.RequestHandler):
    # @tornado.gen.coroutine
    # def post(self):
    #     # getid = tornado.escape.xhtml_escape(self.get_argument("storelike"))
    #     blogid = self.request.arguments
    #     # blogid = dict(blogid)
    #     # blogid = blogid.strip('b')
    #     # blogid = blogid.strip('"+blogid+"')
    #     for key, value in blogid.items():
    #         blogid = key 
        
    #     cursor = yield pool.execute("UPDATE blog_user SET blog_dislike=blog_dislike+1 WHERE blog_id= '"+blogid+"';")
    # cursor.close()
    
    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        feedbackid = ''.join(random.choice(string.ascii_letters) for i in range(10))
        review_dislike = self.get_secure_cookie("user")
        review_dislike = review_dislike.decode('ASCII')

        for key, values in blogid.items():
            blogid = key
        blogid = blogid[3:]
        print(blogid)
        cursor = yield pool.execute("INSERT INTO `blog_likes` (`blog_dislike`, `blog_id`, `action_id`) VALUES ('"+review_dislike+"', '"+blogid+"', '"+feedbackid+"');")
        cursor.close()
        cursor = yield pool.execute("SELECT blog_dislike from blog_user WHERE blog_id= '"+blogid+"';")
        dislike_count = cursor.fetchall()
        cnt=0
        cursor.close()
        if dislike_count[0][0] is None:
            cnt=1
            cursor = yield pool.execute("UPDATE blog_user SET blog_dislike=1 WHERE blog_id= '"+blogid+"';")
        else:
            cnt=dislike_count[0][0]+1
            cursor = yield pool.execute("UPDATE blog_user SET blog_dislike=blog_dislike+1 WHERE blog_id= '"+blogid+"';")
        self.xsrf_token
        cursor.close()
        self.write(json.dumps({"status": "ok", "sent": blogid,"cnt":cnt}))

        self.finish()



class DeleteDisLikeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        delete_dislike = self.get_secure_cookie("user")
        delete_dislike = delete_dislike.decode('ASCII')
        for key, values in blogid.items():
            blogid = key
        blogid = blogid[3:]
        # useful code goes here
        cursor = yield pool.execute("UPDATE blog_user SET blog_dislike=blog_dislike-1 WHERE blog_id= '"+blogid+"';")
        cursor.close()
        cursor = yield pool.execute("SELECT blog_dislike from blog_user WHERE blog_id= '"+blogid+"';")
        dislike_count = cursor.fetchall()
        cursor = yield pool.execute("DELETE FROM blog_likes WHERE blog_id = '"+blogid+"' and blog_dislike = '"+delete_dislike+"'")
        cursor.close()
        self.xsrf_token
        print(dislike_count)
        self.write(json.dumps({"status": "ok", "sent": blogid,"cnt":dislike_count[0][0]}))

        self.finish()

class PostEditHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        post = self.request.arguments
        
        blogid = post['data']
        blogid = blogid[0].decode("ASCII")
        self.set_secure_cookie("blogid", blogid)
        print(blogid)

    @tornado.gen.coroutine
    def post(self):
        # getid = tornado.escape.xhtml_escape(self.get_argument("storelike"))
        post = self.request.arguments
        for key, value in post.items():
            desc = value

        desc = desc[0].decode("ASCII")

        blogid = self.get_secure_cookie("blogid")
        blogid = blogid.decode("ASCII")
        cursor = yield pool.execute("UPDATE blog_user SET blog_desc='"+desc+"' WHERE blog_id= '"+blogid+"';")
        self.xsrf_token
        cursor.close()


class UserFullPostHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        blogid = self.request.arguments
        for key, value in blogid.items():
            blogid = key   
        print(blogid)  
        data = yield pool.execute("Select * from blog_user WHERE blog_id = '"+blogid+"';")
        data = data.fetchall()
        print(data)
        self.render("singlepost.html" , data = data)
        
        

class CatagoryTechHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):    
        cursor = yield pool.execute("Select * from blog_user WHERE blog_category = 'tech';")
        data = cursor.fetchall()
        self.render("category.html" , entries = data)




class CommentPostHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        getcomment = tornado.escape.xhtml_escape(self.get_argument("comment"))
        get_current_user_email = self.get_secure_cookie("user")
        get_current_user_email = get_current_user_email.decode("ASCII")
        get_blog_id = tornado.escape.xhtml_escape(self.get_argument("blogid"))
        cursor = yield pool.execute("INSERT INTO `blog_comment` ( `blog_id`, `blog_comments` ,`user_email`) VALUES ('"+get_blog_id+"', '"+getcomment+"', '"+get_current_user_email+"' );")
        cursor.close()

        cursor = yield pool.execute("Select * from blog_user WHERE blog_id = '"+get_blog_id+"'")
        single = yield pool.execute("Select * from blog_comment WHERE blog_id = '"+get_blog_id+"'")
        singleblog  = cursor.fetchall() 
        comment = single.fetchall()
        data = [singleblog , comment] 
        self.render("single-post-2.html" , data = data)

class MyPostHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        useremail = str(self.get_secure_cookie("user"))
        useremail = useremail.strip('b')
        getuseremail = useremail.strip('"+useremail+"')    
        cursor = yield pool.execute("Select * from blog_user WHERE user_email = "+getuseremail+";")
        data = cursor.fetchall()
        self.render("userpost.html" , entries = data)

class CatagoryMusicHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):    
        cursor = yield pool.execute("Select * from blog_user WHERE blog_category = 'music'")
        data = cursor.fetchall()
        self.render("category.html" , entries = data)

class CatagoryPoliticsHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):    
        cursor = yield pool.execute("Select * from blog_user WHERE blog_category = 'political'")
        data = cursor.fetchall()
        self.render("category.html" , entries = data)

class AboutUsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("about.html")

       
class CreateBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("createblog.html")

class StoreinDbHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        gettitle = tornado.escape.xhtml_escape(self.get_argument("title"))
        getauthor = tornado.escape.xhtml_escape(self.get_argument("author"))
        getdesc = tornado.escape.xhtml_escape(self.get_argument("desc"))
        getcatagory = tornado.escape.xhtml_escape(self.get_argument("catagory"))
        getimage = tornado.escape.xhtml_escape(self.get_argument("fileupload"))
        # Image = self.get_body_argument("fileupload")

        useremail = str(self.get_secure_cookie("user"))
        useremail = useremail.strip('b')
        getemail = useremail.strip('"+useremail+"')
        cursor = yield pool.execute("INSERT INTO `blog_user` (`blog_title`, `blog_author`, `blog_desc` ,`blog_category` ,`user_email` ,`image_link`) VALUES ('"+gettitle+"', '"+getauthor+"', '"+getdesc+"' , '"+getcatagory+"', "+getemail+" , '"+getimage+"' );")
        cursor.close()
        time.sleep(5)
        self.redirect(self.get_argument("next", self.reverse_url("main")))


class DeletePostHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        post = self.request.arguments
        blogid = post['data']
        blogid = blogid[0].decode("ASCII")
        # self.set_secure_cookie("blogid", blogid)
        cursor = yield pool.execute("DELETE FROM blog_user WHERE blog_id ='"+blogid+"'")
        cursor1 = yield pool.execute("DELETE FROM blog_likes WHERE blog_id ='"+blogid+"'")
        cursor2 = yield pool.execute("DELETE FROM blog_comment WHERE blog_id ='"+blogid+"'")
        cursor.close()
        cursor1.close()
        cursor2.close()
        self.reverse_url("mypost")

class RegisterHandler(LoginHandler):
    @tornado.gen.coroutine
    def get(self):
        msg=''
        self.render('register.html',msg=msg)
    @tornado.gen.coroutine
    def post(self):
        getemail = tornado.escape.xhtml_escape(self.get_argument("email"))
        print(getemail)
        cursor = yield pool.execute("Select * from users_details where user_emai='"+getemail+"'")
        cursor.close()
        already_taken = cursor.rowcount
        
        if already_taken:
            msg = "404"
            error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
            self.render("register.html", msg=msg)
            
            return
        #Warning bcrypt will block IO loop:
        # password = self.get_argument("password").encode('utf-8')
        # hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt(8))
        
        getemail = tornado.escape.xhtml_escape(self.get_argument("email"))
        username = tornado.escape.xhtml_escape(self.get_argument("username"))
        password = tornado.escape.xhtml_escape(self.get_argument("password"))
        password = password.encode('utf-8')
        pass1 = hashlib.sha1(password).digest()
        pass2 = hashlib.sha1(pass1).hexdigest()
        pass2 = "*" + pass2.upper()
        cursor = yield pool.execute("INSERT INTO `users_details` ( `user_name`, `user_password`, `user_emai`) VALUES ('"+username+"', '"+pass2+"' ,'"+getemail+"');")
        cursor.close()
        self.redirect(self.get_argument("next", self.reverse_url("main")))
 


class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login",
            'template_path': os.path.join(base_dir, "templates"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": False,
        }
        
        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/home", MainHandler, name="main"),
            tornado.web.url(r'/login', LoginHandler, name="login"),
            tornado.web.url(r'/logout', LogoutHandler, name="logout"),
            tornado.web.url(r'/register', RegisterHandler, name="register"),
            tornado.web.url(r'/forgot', ForgotHandler, name="forgot"),
            tornado.web.url(r'/profile', ProfileHandler, name="profile"),
            tornado.web.url(r'/createblog', CreateBlogHandler, name="createblog"),
            tornado.web.url(r'/storeindb', StoreinDbHandler, name="storeindb"),
            tornado.web.url(r'/storelike', StoreLikeHandler, name="storelike"),
            tornado.web.url(r'/deletelike', DeleteLikeHandler, name="deletelike"),
            tornado.web.url(r'/storedislike', StoreDisLikeHandler, name="storedislike"),
            tornado.web.url(r'/deletedislike', DeleteDisLikeHandler, name="deletedislike"),
            tornado.web.url(r'/catagory/tech', CatagoryTechHandler, name="tech"),
            tornado.web.url(r'/catagory/music', CatagoryMusicHandler, name="music"),
            tornado.web.url(r'/catagory/political', CatagoryPoliticsHandler, name="political"),
            tornado.web.url(r'/auth/home/user/mypost', MyPostHandler, name="mypost"),
            tornado.web.url(r'/auth/home/user/mypost/edit', PostEditHandler, name="edit"),
            tornado.web.url(r'/auth/home/posts/fullpost', UserFullPostHandler, name="userfullpost"),
            tornado.web.url(r'/commentstoreindb', CommentPostHandler, name="comment"),
            tornado.web.url(r'/deletepost', DeletePostHandler, name="deletepost"),
            tornado.web.url(r'/info/edu', AboutUsHandler, name="aboutus")
            
], **settings, default_handler_class=My404Handler)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    print("Application running on localhost:" + str(options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()