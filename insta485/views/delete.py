"""
Insta485 index (main) view.

URLs include:
/accounts/delete/
"""
import flask
import insta485
from insta485.views.helpers import login_required_redirect


@insta485.app.route('/accounts/delete/')
@login_required_redirect
def show_delete():
    """Display delete page."""
    logname = flask.session["username"]
    context = {
        "logname": logname
    }

    return flask.render_template("delete.html", **context)
