"""
Insta485 index (main) view.

URLs include:
/accounts/?target=URL
"""
import flask
import insta485

@insta485.app.route('/accounts/', methods=["POST"])
def handle_account():
    """Update accounts"""
    
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    """

    logname = "awdeorio"

    connection = insta485.model.get_db()

    operation = flask.request.form.get("operation")
    target = flask.request.args.get("target", "/")
    username = flask.request.form.get("username")
    if operation == "follow":
        if (already follow){
            flask.abort(409)
        }
        connection.execute(
        "INSERT INTO following (username1, username2) VALUES (?, ?)",
        (logname, username)
        )
    elif operation == "unfollow":
        if (alreadu unfollow){
            flask.abort(409)
        }
        cur = connection.execute(
        "SELECT owner FROM comments WHERE commentid = ?", (commentid,)
        )
    
    return flask.redirect(target)