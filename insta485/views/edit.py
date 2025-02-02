"""
Insta485 index (main) view.

URLs include:
/accounts/edit/
"""
import flask
import insta485
from insta485.views.helpers import get_logged_in_user, NotLoggedIn


@insta485.app.route('/accounts/edit/')
def show_edit():
    """Display edit page."""
    try:
        logname = get_logged_in_user()
    except NotLoggedIn:
        return flask.redirect("/accounts/login/")

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT email, fullname, filename FROM users WHERE username = ?",
        (logname,)
    )

    user = cur.fetchone()

    context = {
        "email": user["email"],
        "fullname": user["fullname"],
        "username": logname,
        "profilepic": user["filename"],
    }
    insta485.model.close_db(error=None)
    return flask.render_template("edit.html", **context)
