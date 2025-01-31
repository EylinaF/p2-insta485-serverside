"""
Insta485 index (main) view.

URLs include:
/users/<user_url_slug>/following/
"""
import flask
import insta485
LOGGER = flask.logging.create_logger(insta485.app)
@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """Display user following page."""

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']

    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (user_url_slug,)
    )
    user = cur.fetchone()

    if user is None:
        flask.abort(404)

    cur = connection.execute(
        """
        SELECT users.username, users.filename AS user_img_url
        FROM following
        JOIN users ON following.username2 = users.username
        WHERE following.username1 = ?
        """,
        (user_url_slug,)
    )
    following = cur.fetchall()

    for follow in following:
        follow["user_img_url"] = f"/uploads/{follow['user_img_url']}"
        
        cur = connection.execute(
        "SELECT 1 FROM following WHERE username1 = ? AND username2 = ?",
        (follow["username"], logname)
        )
        follow["logname_follows_username"] = cur.fetchone() is not None

    context = {
        "logname": logname,
        "username": user_url_slug,
        "following": following,
    }
    insta485.model.close_db(error = None)
    return flask.render_template("following.html", **context)