"""
Insta485 index (main) view.

URLs include:
/comments/?target=URL
"""
import flask
import insta485
LOGGER = flask.logging.create_logger(insta485.app)
@insta485.app.route('/comments/', methods=["POST"])
def handle_comments():
    """Update comments"""
    

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    
    logname = flask.session['username']


    connection = insta485.model.get_db()

    operation = flask.request.form.get("operation")
    target = flask.request.args.get("target", "/")
    postid = flask.request.form.get("postid")
    commentid = flask.request.form.get("commentid")
    text = flask.request.form.get("text", "").strip()
    LOGGER.debug("operation = %s", operation)
    LOGGER.debug("postid = %s", postid)
    LOGGER.debug("commentid = %s", commentid)
    LOGGER.debug("text = %s", text)

    if operation == "create":
        if not text:
            flask.abort(400)
        
        connection.execute(
        "INSERT INTO comments (commentid, owner, postid, text) VALUES (?, ?, ?, ?)",
        (commentid, logname, postid, text)
        )
    elif operation == "delete":
        cur = connection.execute(
        "SELECT owner FROM comments WHERE commentid = ?", (commentid,)
        )
        owner = cur.fetchone

        """
        if owner != logname:
            flask.abort(403)
        """
        
        
        connection.execute("DELETE FROM comments WHERE commentid = ?", (commentid,))
    insta485.model.close_db(error = None)
    return flask.redirect(target)


    
