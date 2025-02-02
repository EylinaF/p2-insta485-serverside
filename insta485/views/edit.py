"""
Insta485 index (main) view.

URLs include:
/accounts/edit/
"""
import flask
import insta485
from insta485.views.helpers import login_required_redirect


@insta485.app.route('/accounts/edit/')
@login_required_redirect
def show_edit():
    """Display edit page."""
    logname = flask.session["username"]

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT email, fullname, filename FROM users WHERE username = ?",
        (logname,)
    )

    user = cur.fetchone()
    user["filename"] = f"/uploads/{user["filename"]}"
    context = {
        "email": user["email"],
        "fullname": user["fullname"],
        "username": logname,
        "profilepic": user["filename"],
    }
    insta485.model.close_db(error=None)
    return flask.render_template("edit.html", **context)
