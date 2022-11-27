from flask import Flask, render_template
from markupsafe import escape
app = Flask(__name__)


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
