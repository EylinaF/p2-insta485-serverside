"""
Insta485 index (main) view.

URLs include:
/accounts/password/
"""
import flask
import insta485


@insta485.app.route('/accounts/password/')
def show_password():
    """Display password page."""

    return flask.render_template("delete.html")
