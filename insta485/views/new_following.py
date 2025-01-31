"""
Insta485 index (main) view.

URLs include:
/following/?target=URL
"""
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)

@insta485.app.route('/following/', methods=["POST"])
def handle_following():
    """Update following"""

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']


    connection = insta485.model.get_db()

    operation = flask.request.form.get("operation")
    target = flask.request.args.get("target", "/")
    username = flask.request.form.get("username")
    LOGGER.debug("operation = %s", operation)
    LOGGER.debug("username = %s", username)
    if operation == "follow":
        cur = connection.execute(
            "SELECT 1 FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username)
        )

        if cur.fetchone():
            flask.abort(409)

        connection.execute(
        "INSERT INTO following (username1, username2) VALUES (?, ?)",
        (logname, username)
        )
    elif operation == "unfollow":
        cur = connection.execute(
            "SELECT 1 FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username)
        )
        if not cur.fetchone():
            flask.abort(409)

        connection.execute(
            "DELETE FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username)
        )
    
    return flask.redirect(target)