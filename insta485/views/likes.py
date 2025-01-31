"""Like and Unlike Post View."""
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route("/likes/", methods=["POST"])
def update_likes():
    """Handle liking and unliking a post."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']

    operation = flask.request.form.get("operation")
    postid = flask.request.form.get("postid")
    target_url = flask.request.args.get("target", "/")

    LOGGER.debug("operation = %s", operation)
    LOGGER.debug("postid = %s", postid)

    # Connect to database
    connection = insta485.model.get_db()


    cur = connection.execute("SELECT 1 FROM posts WHERE postid = ?", (postid,))
    if cur.fetchone() is None:
        flask.abort(404)

    if operation == "like":
        cur = connection.execute(
            "SELECT 1 FROM likes WHERE postid = ? AND owner = ?",
            (postid, logname),
        )
        if cur.fetchone():
            flask.abort(409)


        connection.execute(
            "INSERT INTO likes (owner, postid) VALUES (?, ?)",
            (logname, postid),
        )

    elif operation == "unlike":
        cur = connection.execute(
            "SELECT 1 FROM likes WHERE postid = ? AND owner = ?",
            (postid, logname),
        )
        if cur.fetchone() is None:
            flask.abort(409)


        connection.execute(
            "DELETE FROM likes WHERE postid = ? AND owner = ?",
            (postid, logname),
        )

    else:
        flask.abort(400) 

    insta485.model.close_db()
    return flask.redirect(target_url)
