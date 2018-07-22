from models import db, User
from forms import SignupForm, LoginForm, ForgotPassword, AddImage
from flask import Flask, url_for, render_template, request, redirect, session, send_from_directory
import smtplib
import string
from random import *
from werkzeug import generate_password_hash
from sendEmail import sendEmail
from filter import crop, flip, gray
from flask_bootstrap import Bootstrap
from PIL import Image
from werkzeug.utils import secure_filename
import os
from filter import crop, flip, gray, galaxy
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)
filename = "NULL"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shreya@localhost/postgres'
db.init_app(app)
app.secret_key = "development-key"

Bootstrap(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(APP_ROOT, 'images')
thumbnails_directory = os.path.join(APP_ROOT, 'thumbnails')
@app.route("/")
def index():
  #session['username'] = None
  return render_template("/index1.html")

@app.route("/test")
def testpage():
  return render_template("/page30.html")

@app.route("/nearest")
def nearesr_store():
  return render_template("/NearestStores.html")

@app.route("/about")
def about():
  return render_template("/about.html")

@app.route('/add/', methods = ['GET', 'POST'])
def add():
    form = AddImage()
    if request.method == 'POST':
        print("if loop")
        # print(request.files['user_image'])
        if form.validate_on_submit():
            print("in second if")
            for upload in request.files['user_image']:
                print("in for loop")
                filename = upload.filename
                url = upload.url(filename)
                new_image = Image(filename,url)
                db.session.add(new_image)
                db.session.commit()
    return render_template('add.html', form=form)

UPLOADS_DEFAULT_DEST = images_directory
UPLOADS_DEFAULT_URL = 'http://localhost:5000/images/'

UPLOADED_IMAGES_DEST = thumbnails_directory
UPLOADED_IMAGES_URL = 'http://localhost:5000/thumbnails/'
# Configure the image uploading via Flask-Uploads
images = UploadSet('userImages', IMAGES)
# configure_uploads(app, images)

@app.route('/signup.html', methods=["GET"])
def signupPage():
  form = SignupForm()
  return render_template('/signup.html',form=form)

@app.route("/signup/", methods=["POST"])
def signup():
  form = SignupForm()
  logform = LoginForm()
  if request.method == "POST":
    #print(form.validate())
    if form.validate() == False:
      #print("here")
      return render_template('/signup.html', form=form)
      #return 'Error'
    else:
      #print("in else")
      newuser = User(form.user_name.data, form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      return render_template('/login.html',form=logform)
    return render_template('/signup.html')
  #
  # elif request.method == "GET":
  #   return render_template('/signup.html', form=form)

@app.route('/login.html')
def loginPage():
    form = LoginForm()
    return render_template('/login.html',form=form)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
  form = LoginForm()
  print(request.method)
  if request.method == "POST":
    if form.validate() == False:
      print(form.validate())
      return render_template("login.html", form = form)
    else :
      print("in else")
      user_name = form.user_name.data
      password = form.password.data
      user = User.query.filter_by(username = user_name).first()
      if user is not None and user.check_password(password):
        session['username'] = form.user_name.data
        print(form.user_name.data)
        session['logged_in']=True
        return redirect(url_for('index'))
      else :
        return redirect(url_for('login'))
  return render_template('/error.html',message="Opps...Login Error. Please try again!")

@app.route("/logout.html")
def logout():
  session.pop('username', None)
  session['logged_in']=False
  return redirect(url_for('index'))

@app.route("/forgotpassword/",methods=["POST"])
def forgotpassword():
  form=ForgotPassword()
  user_name = form.user_name.data
  user = User.query.filter_by(username = user_name).first()
  if user is not None:
    allchar = string.ascii_letters + string.digits
    newpassword = "".join(choice(allchar) for x in range(randint(6,12)))
    msg = "your new password is" + newpassword
    print(msg)
    print(user.email)
    hashedpass=generate_password_hash(newpassword)
    admin = User.query.filter_by(username=user_name).update(dict(password=hashedpass))
    db.session.commit()
    msg="Your new Password is" + newpassword
    if sendEmail(user.email,"Password Reset",msg):
      return render_template('/error.html',message="Email sent to "+user.email)
    else:
      return render_template('/error.html',message="Error when email sent to "+user.email)
  else:
     return render_template('/error.html',message="User does not Exsist")

@app.route('/linkage')
def link():
    return render_template('link.html')

@app.route('/gallery')
def gallery():
    if session['logged_in']:
        thumbnail_names = os.listdir('./thumbnails')
        return render_template('gallery.html', thumbnail_names=thumbnail_names)
    else:
        form = LoginForm()
        return render_template('/login.html',form=form)


@app.route('/thumbnails/<filename>')
def thumbnails(filename):
    return send_from_directory('thumbnails', filename)

@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/public/<path:filename>')
def static_files(filename):
    return send_from_directory('./public', filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global filename
    if request.method == 'POST':
        for upload in request.files.getlist('images'):
            filename = upload.filename
            # Always a good idea to secure a filename before storing it
            filename = secure_filename(filename)

            # This is to verify files are supported
            ext = os.path.splitext(filename)[1][1:].strip().lower()
            if ext in set(['jpg', 'jpeg', 'png']):
                print('File supported moving on...')
            else:
                return render_template('error.html', message='Uploaded files are not supported...')
            destination = '/'.join([images_directory, filename])
            # Save original image
            upload.save(destination)
            # Save a copy of the thumbnail image
            #image = Image.open(destination)
            #image.thumbnail((300, 170))
            #image_black = image.convert('L')
            #image_black.save('gray.jpg')
            #image_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
            #image_flip.save('image_flip.jpg')
            #image.save('/'.join([thumbnails_directory, filename]))
            #image_black.save('/'.join([thumbnails_directory, 'gray.jpg']))
        #return redirect(url_for('gallery'))
    return render_template('upload.html',image_name=filename)

@app.route('/forgotpassword.html', methods=["GET"])
def forgotpasswordpage():
  form = ForgotPassword()
  return render_template('/forgotpassword.html',form=form)

@app.route('/gray/<filename>', methods=['GET', 'POST'])
def grayfilter(filename):
    destination = '/'.join([images_directory, filename])
    #print(destination)
    image_gray=gray(destination=destination)
    image_gray.save('/'.join([thumbnails_directory, filename]))
    return redirect(url_for('gallery'))

@app.route('/flip/<filename>', methods=['GET', 'POST'])
def flipfilter(filename):
    destination = '/'.join([images_directory, filename])
        #print(destination)
    image_flip=flip(destination=destination)
    image_flip.save('/'.join([thumbnails_directory, filename]))
    return redirect(url_for('gallery'))

@app.route('/crop/<filename>', methods=['GET', 'POST'])
def cropfilter(filename):
    destination = '/'.join([images_directory, filename])
        #print(destination)
    image_crop=crop(destination=destination)
    image_crop.save('/'.join([thumbnails_directory, filename]))
    return redirect(url_for('gallery'))
@app.route('/galaxy/<filename>', methods=['GET', 'POST'])
def galaxyfilter(filename):
    destination = '/'.join([images_directory, filename])
        #print(destination)
    image_galaxy=crop(destination=destination)
    image_galaxy.save('/'.join([thumbnails_directory, filename]))
    return redirect(url_for('gallery'))

if __name__ == "__main__":
  app.run(debug=True)
