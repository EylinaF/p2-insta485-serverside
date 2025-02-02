"""
Insta485 index (main) view.

URLs include:
/accounts/delete/
"""
import flask
import insta485
from insta485.views.helpers import get_logged_in_user, NotLoggedIn


@insta485.app.route('/accounts/delete/')
def show_delete():
    """Display delete page."""
    try:
        logname = get_logged_in_user()
    except NotLoggedIn:
        return flask.redirect("/accounts/login/")
    context = {
        "logname": logname
    }

    return flask.render_template("delete.html", **context)
