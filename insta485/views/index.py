"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485
from insta485.views.helpers import login_required_redirect


@insta485.app.route('/')
@login_required_redirect
def show_index():
    """Display / route."""
    logname = flask.session["username"]

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        """
        SELECT posts.postid,
            posts.filename AS img_url,
            posts.created AS timestamp,
            users.username AS owner,
            users.filename AS owner_img_url
        FROM posts
        JOIN users ON posts.owner = users.username
        WHERE posts.owner = ? OR posts.owner IN (
        SELECT username2 FROM following WHERE username1 = ?
        )
        ORDER BY posts.postid DESC
        """,
        (logname, logname)
    )
    posts = cur.fetchall()

    for post in posts:
        cur = connection.execute(
            "SELECT COUNT(*) AS like_count FROM likes WHERE postid = ?",
            (post["postid"],)
        )
        post["likes"] = cur.fetchone()["like_count"]

        cur = connection.execute(
            "SELECT 1 FROM likes WHERE postid = ? AND owner = ?",
            (post["postid"], logname)
        )
        post["liked_by_user"] = cur.fetchone() is not None

        cur = connection.execute(
            """
            SELECT users.username AS owner, comments.text
            FROM comments
            JOIN users ON comments.owner = users.username
            WHERE comments.postid = ?
            ORDER BY comments.created ASC
            """,
            (post["postid"],)
        )

        post["comments"] = cur.fetchall()
        post["img_url"] = f"/uploads/{post['img_url']}"
        post["owner_img_url"] = f"/uploads/{post['owner_img_url']}"
        post["timestamp"] = arrow.get(post["timestamp"]).humanize()

    context = {
        "logname": logname,
        "posts": posts,
    }
    insta485.model.close_db(error=None)
    return flask.render_template("index.html", **context)
