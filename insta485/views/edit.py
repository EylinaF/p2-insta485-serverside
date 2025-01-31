"""
Insta485 index (main) view.

URLs include:
/accounts/edit/
"""
import flask
import insta485

@insta485.app.route('/accounts/edit/')
def show_edit():
    """Display edit page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('/accounts/login/'))

    logname = flask.session['username']

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT email, fullname, p FROM users WHERE username = ?",
        (logname,)
    )
    context = {
        "email": email,
        "fullname": fullname,
        "username": user_url_slug,
        "profilepic": profilepic,
    }

    return flask.render_template("create.html", **context)