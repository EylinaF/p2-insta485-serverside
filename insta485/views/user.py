"""
Insta485 index (main) view.

URLs include:
/users/<user_url_slug>/
"""
import flask
import insta485
from insta485.views.helpers import login_required_redirect


@insta485.app.route('/users/<user_url_slug>/')
@login_required_redirect
def show_user_profile(user_url_slug):
    """Display user profile page."""
    logname = flask.session["username"]

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (user_url_slug,)
    )
    user = cur.fetchone()

    if user is None:
        flask.abort(404)

    cur = connection.execute(
        "SELECT COUNT(*) AS total_posts FROM posts WHERE owner = ?",
        (user_url_slug,)
    )
    total_posts = cur.fetchone()["total_posts"]

    cur = connection.execute(
        "SELECT COUNT(*) AS followers FROM following WHERE username2 = ?",
        (user_url_slug,)
    )
    followers = cur.fetchone()["followers"]

    cur = connection.execute(
        "SELECT COUNT(*) AS following FROM following WHERE username1 = ?",
        (user_url_slug,)
    )
    following = cur.fetchone()["following"]

    cur = connection.execute(
        "SELECT 1 FROM following WHERE username1 = ? AND username2 = ? ",
        (logname, user_url_slug)
    )

    logname_follows_username = cur.fetchone() is not None

    cur = connection.execute(
        """
        SELECT posts.postid, posts.filename AS img_url
        FROM posts
        WHERE posts.owner = ?
        ORDER BY posts.postid DESC
        """,
        (user_url_slug,)
    )
    posts = cur.fetchall()

    for post in posts:
        post["img_url"] = f"/uploads/{post['img_url']}"

    context = {
        "logname": logname,
        "username": user["username"],
        "logname_follows_username": logname_follows_username,
        "fullname": user["fullname"],
        "following": following,
        "followers": followers,
        "total_posts": total_posts,
        "posts": posts,
    }
    insta485.model.close_db(error=None)
    return flask.render_template("user.html", **context)
