from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# ✅ LoginManager 구성
login_manager = LoginManager()
login_manager.login_view = "login"  # 로그인 안 된 상태로 보호된 경로 접근 시 이동할 뷰
login_manager.init_app(app)


@app.context_processor
def inject_user():
    return dict(logged_in=current_user.is_authenticated)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# User 모델
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    if not email or not password or not name:
        flash("Please fill out all fields", "error")
        return redirect(url_for('register'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered", "error")
        return redirect(url_for('register'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    new_user = User()
    new_user.email = email
    new_user.password = hashed_password
    new_user.name = name

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('secrets'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("secrets"))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/secrets')
@login_required  # ✅ 인증된 사용자만 접근 가능
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route('/download')
@login_required  # ✅ 인증된 사용자만 파일 다운로드 가능
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf')


@app.route('/logout')
@login_required  # ✅ 인증된 사용자만 로그아웃 가능
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
