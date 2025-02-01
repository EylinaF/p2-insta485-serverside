"""
Posts.

URL is.
"""
import flask
import arrow
import insta485


@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    """Serve uploaded files only to authenticated users."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']

    connection = insta485.model.get_db()
    cur = connection.execute(
        """
        SELECT posts.postid,
                posts.filename AS img_url,
                posts.created AS timestamp,
                users.username,
                users.filename AS owner_img_url
        FROM posts
        JOIN users ON posts.owner = users.username
        WHERE posts.postid = ?
        """,
        (postid_url_slug,)
    )
    post = cur.fetchone()

    if post is None:
        flask.abort(404)

    cur = connection.execute(
        """
        SELECT COUNT(*) AS like_count FROM likes WHERE postid = ?
        """,
        (post["postid"],)
    )
    post["likes"] = cur.fetchone()["like_count"]

    cur = connection.execute(
        """
        SELECT 1 FROM likes WHERE postid = ? AND owner = ?
        """,
        (post["postid"], logname)
    )
    post["liked_by_user"] = cur.fetchone() is not None

    cur = connection.execute(
        """
        SELECT users.username AS owner, comments.text, comments.commentid
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
        "postid": post["postid"],
        "owner": post["username"],
        "owner_img_url": post["owner_img_url"],
        "img_url": post["img_url"],
        "timestamp": post["timestamp"],
        "likes": post["likes"],
        "liked_by_user": post["liked_by_user"],
        "comments": post["comments"]
    }
    insta485.model.close_db(error=None)
    return flask.render_template("post.html", **context)
