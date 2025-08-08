from datetime import datetime
from app import db
from flask_login import UserMixin

# ------------------------------
# Modelo Usuario
# ------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relaciones
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __str__(self):
        return self.username


# ------------------------------
# Modelo Categoría
# ------------------------------
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relaciones
    posts = db.relationship('Post', backref='category', lazy=True)

    def __str__(self):
        return self.name


# ------------------------------
# Modelo Post / Entrada
# ------------------------------
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Claves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Relaciones
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __str__(self):
        return f'{self.title} ({self.author.username})'


# ------------------------------
# Modelo Comentario
# ------------------------------
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Claves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __str__(self):
        return f'Comentario de {self.author.username} en post #{self.post_id}'
