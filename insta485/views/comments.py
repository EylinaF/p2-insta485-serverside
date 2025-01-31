"""
Insta485 index (main) view.

URLs include:
/comments/?target=URL
"""
import flask
import insta485

@insta485.app.route('/comments/', methods=["POST"])
def handle_comments():
    """Update comments"""
    
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    """

    logname = "awdeorio"

    connection = insta485.model.get_db()

    operation = flask.request.form.get("operation")
    target = flask.request.args.get("target", "/")
    postid = flask.request.form.get("postid")
    commentid = flask.request.form.get("commentid")
    text = flask.request.form.get("text", "").strip()

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
    
    return flask.redirect(target)


    
