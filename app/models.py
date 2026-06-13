from .                          import db
from flask_login                import UserMixin
from sqlalchemy.sql             import func
from werkzeug.datastructures    import FileStorage
from werkzeug.utils             import secure_filename

with open("app/images/6p915t-modified.jpg", 'rb') as f:
    upload = FileStorage(f, '6p915t-modified.jpg', name='file', content_type='image/jpg')
    filenames = secure_filename(upload.filename)
    mimetypes = upload.mimetype
    imgs = upload.read()
    
class Newspost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userupload = db.Column(db.String(100))
    
    comments = db.relationship('Commentpost', backref='post', passive_deletes=True)
    likes = db.relationship('Likepost', backref='post', passive_deletes=True)
    
class Pespost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    img = db.Column(db.Text, nullable = False)
    name = db.Column(db.Text, nullable = False)
    mimetype = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userupload = db.Column(db.String(100))
    
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150), unique=True)
    check = db.Column(db.String(5))
    likecount = db.Column(db.Integer, default = 0)
    description = db.Column(db.String(250), default = "")
    color = db.Column(db.String(150), default = "secondary")
    
    friends = db.Column(db.Text, default = "")
    recieved = db.Column(db.Text, default = "")
    mentions = db.Column(db.Text, default = "")
    
    avatar = db.Column(db.Text, default = imgs)
    avatarname = db.Column(db.Text, default = filenames)
    mimetype = db.Column(db.Text, default = mimetypes)
    
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    commentposts = db.relationship('Commentpost', backref='user', passive_deletes=True)
    
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    likespost = db.relationship('Likepost', backref='user', passive_deletes=True)

    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesid = db.Column(db.Integer, db.ForeignKey('pespost.id', ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    
class Likepost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesid = db.Column(db.Integer, db.ForeignKey('newspost.id', ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    pesid = db.Column(db.Integer, db.ForeignKey('pespost.id', ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Commentpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    pesid = db.Column(db.Integer, db.ForeignKey('newspost.id', ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())