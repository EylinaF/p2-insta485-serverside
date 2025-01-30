"""
Insta485 index (main) view.

URLs include:
/accounts/login/
"""
import flask
import insta485

@insta485.app.route('/accounts/login/')
def show_login():
    """Display login page."""

    if "username" in flask.session:
        return flask.redirect(flask.url_for("show_index"))

    return flask.render_template("login.html")