from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app import db
from models import Category

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField('Contenido', validators=[DataRequired(), Length(min=10)])
    category = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Publicar')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

class CommentForm(FlaskForm):
    content = TextAreaField('Comentario', validators=[DataRequired(), Length(min=3, max=500)])
    submit = SubmitField('Comentar')

class CategoryForm(FlaskForm):
    name = StringField('Nombre de la categoría', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Guardar')
