from flask import Flask, render_template, request
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import dotenv_values

from models import InfoModel, db

config = dotenv_values(".env")
# from models import db, InfoModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['CONNECTION_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()

migrate = Migrate(app, db)


@app.route("/")
def home_route():
    app.logger.debug('Home route hit!')
    return "<p>Hello, Home Route!</p>"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        users = InfoModel.query.all()
        results = [{
            "name": user.name,
            "age": user.age,
            "eye_colour": user.eye_colour,
        } for user in users]
        return {"user count": len(results), "users": results}

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        eye_colour = request.form['eye_colour']
        new_user = InfoModel(name=name, age=age, eye_colour=eye_colour)
        db.session.add(new_user)
        db.session.commit()
        return f"Done!!"


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
