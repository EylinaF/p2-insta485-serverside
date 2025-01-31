"""
Insta485 index (main) view.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Display user following page."""

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']

    # Connect to database
    connection = insta485.model.get_db()
    user = logname

    if user is None:
        flask.abort(404)

    cur = connection.execute(
        """
        SELECT users.username, users.filename AS user_img_url
        FROM users
        WHERE username != ?
        AND username NOT IN (
            SELECT username2 FROM following WHERE username1 = ?
        )
        """,
        (logname, logname)
    )
    expo_users = cur.fetchall()

    for expo_user in expo_users:
        expo_user["user_img_url"] = f"/uploads/{expo_user['user_img_url']}"
        expo_user["profile_url"] = f"/users/{expo_user['username']}/"

    context = {
        "logname": logname,
        "expo_users": expo_users,
    }
    insta485.model.close_db(error=None)
    return flask.render_template("explore.html", **context)
