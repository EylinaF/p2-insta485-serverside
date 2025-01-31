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
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']

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
    return flask.render_template("create.html", **context)
