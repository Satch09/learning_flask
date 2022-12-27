from datetime import timedelta
from flask import Flask, render_template, request, redirect, session
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import dotenv_values
from models.user_model import UserModel, login, db
from flask_login import current_user, login_required, logout_user, login_user

app = Flask(__name__)
config = dotenv_values(".env")
app.secret_key = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['CONNECTION_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
login.login_view = 'login'
login.init_app(app)

migrate = Migrate(app, db)

@app.before_first_request
def create_table():
    db.create_all()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)




@app.route('/blogs')
@login_required
def blog():
    return render_template('blog.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/blogs')

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/blogs')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/blogs')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/blogs')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/blogs')


@app.route("/")
def home_route():
    app.logger.debug('Home route hit!')
    return "<p>Hello, Home Route!</p>"


@app.route("/local/")
@app.route("/local/<person>")
def hello_world(person=None):
    app.logger.debug('A value for debugging (%s has logged in)', person)
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return render_template('foo.html', person=person)


@app.route("/<name>")
def hello_name(name):
    return f"<p>Hello, {escape(name)}!</p>"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


if __name__ == '__main__':
    app.run(debug=True)
