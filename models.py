from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "customer"
    username = db.Column(db.String(120), primary_key=True)
    email = db.Column(db.String(120))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    password = db.Column(db.String(54))

    def __init__(self,username, firstname, lastname, email, password):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<username %r>' % self.password

class Image(db.Model):
    __tablename__ = "images"
    image_filename = db.Column(db.String, default=None, nullable=True, primary_key=True)
    image_url = db.Column(db.String, default=None, nullable=True)

    def __init__(self, title, description):
        self.image_filename = image_filename
        self.image_url = image_url

    def import_data(self, request):
        try:
            if 'user_image' in request.files:
                filename = images.save(request.files['user_image'])
                self.image_filename = filename
                self.image_url = images.url(filename)
        except KeyError as e:
            raise ValidationError('Invalid Image: missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'image_filename': self.image_filename,
            'image_url': self.image_url,
        }


    def __repr__(self):
        return '<title {}'.format(self.name)