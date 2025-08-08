from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inicializar app
app = Flask(__name__)
app.secret_key = 'cualquiercosa'

# Configuración base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root2205@localhost/py_efi1_db"

# Inicializar extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importar modelos
from models import User, Post, Comment, Category

# -------------------------------
# LOGIN MANAGER
# -------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------------
# CONTEXT PROCESSOR (categorías globales)
# -------------------------------
@app.context_processor
def inject_categories():
    return dict(categories=Category.query.all())


# -------------------------------
# RUTAS
# -------------------------------

@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)


@app.route('/foro')
@login_required
def foro():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('foro.html', posts=posts)


@app.route('/mi_perfil')
@login_required
def mi_perfil():
    return render_template('mi_perfil.html')


# -------------------------------
# AUTENTICACIÓN
# -------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Inicio de sesión exitoso. ¡Bienvenido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user_exists = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if user_exists:
            flash('El nombre de usuario o email ya están registrados.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado con éxito. Inicia sesión para continuar.', 'success')
            return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))


# -------------------------------
# POSTS
# -------------------------------

@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category_id')

        post = Post(title=title, content=content, author=current_user, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash('Post creado correctamente.', 'success')
        return redirect(url_for('foro'))

    return render_template('posts/create_post.html')


@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form['comment']
        comment = Comment(content=content, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comentario añadido.', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('posts/post_detail.html', post=post)


# -------------------------------
# MAIN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
