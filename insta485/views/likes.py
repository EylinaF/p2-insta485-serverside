"""Like and Unlike Post View."""
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route("/likes/", methods=["POST"])
def update_likes():
    """Handle liking and unliking a post."""
    #logname = flask.session.get("username")
    logname = "awdeorio"
    if not logname:
        flask.abort(403)  # Unauthorized if not logged in

    # Get form data
    operation = flask.request.form.get("operation")
    postid = flask.request.form.get("postid")
    target_url = flask.request.args.get("target", "/")

    LOGGER.debug("operation = %s", operation)
    LOGGER.debug("postid = %s", postid)

    # Connect to database
    connection = insta485.model.get_db()

    # Check if the post exists
    cur = connection.execute("SELECT 1 FROM posts WHERE postid = ?", (postid,))
    if cur.fetchone() is None:
        flask.abort(404)  # Post not found

    if operation == "like":
        # Check if user already liked the post
        cur = connection.execute(
            "SELECT 1 FROM likes WHERE postid = ? AND owner = ?",
            (postid, logname),
        )
        if cur.fetchone():
            flask.abort(409)  # Conflict: Already liked

        # Insert new like
        connection.execute(
            "INSERT INTO likes (owner, postid) VALUES (?, ?)",
            (logname, postid),
        )

    elif operation == "unlike":
        # Check if user has liked the post
        cur = connection.execute(
            "SELECT 1 FROM likes WHERE postid = ? AND owner = ?",
            (postid, logname),
        )
        if cur.fetchone() is None:
            flask.abort(409)  # Conflict: Not yet liked

        # Delete the like
        connection.execute(
            "DELETE FROM likes WHERE postid = ? AND owner = ?",
            (postid, logname),
        )

    else:
        flask.abort(400)  # Bad request if operation is invalid

    # Redirect to target URL
    return flask.redirect(target_url)
