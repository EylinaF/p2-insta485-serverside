"""
Insta485 index (main) view.

URLs include:
/users/<user_url_slug>/followers/
"""
import flask
import insta485

@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """Display user following page."""


    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('/accounts/login/'))

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
        JOIN users ON following.username1 = users.username
        WHERE following.username2 = ?
        """,
        (user_url_slug,)
    )
    followers = cur.fetchall()

    for follower in followers:
        follower["user_img_url"] = f"/uploads/{follower['user_img_url']}"

        cur = connection.execute(
        "SELECT 1 FROM following WHERE username1 = ? AND username2 = ?",
        (logname, follower["username"])
        )
        follower["logname_follows_username"] = cur.fetchone() is not None

    context = {
        "logname": logname,
        "username": user_url_slug,
        "followers": followers,
    }

    return flask.render_template("followers.html", **context)