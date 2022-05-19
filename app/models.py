from email.policy import default
from app import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy




db=SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(255))
    posts = db.relationship('Post', backref = 'user', lazy = 'dynamic' )
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

   

    def save_user(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'{self.username}'

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    post = db.Column(db.String(99999))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    date = db.Column(db.DateTime, default = datetime.utcnow)

    

    
    def save_post(self):
        db.session.add(self)
        db.session.commit()

    

    def delete_post(self):

        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.id}'


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    pitch_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.Column(db.String(255))


    def save_comment(self,comment):
        db.session.add(comment)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments

