"""
Insta485 following (main) view.

URLs include:
/users/<user_url_slug>/following/
"""
import flask
import insta485
from insta485.views.helpers import get_follow_data
from insta485.views.helpers import login_required_redirect

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route('/users/<user_url_slug>/following/')
@login_required_redirect
def show_following(user_url_slug):
    """Display user following page."""
    logname = flask.session["username"]

    # Connect to database
    connection = insta485.model.get_db()
    following = get_follow_data(user_url_slug, "following")

    for follow in following:
        follow["user_img_url"] = f"/uploads/{follow['user_img_url']}"

        cur = connection.execute(
            "SELECT 1 FROM following WHERE username1 = ? AND username2 = ?",
            (logname, follow["username"])
        )
        follow["logname_follows_username"] = cur.fetchone() is not None

    context = {
        "logname": logname,
        "username": user_url_slug,
        "following": following,
    }
    insta485.model.close_db(error=None)
    return flask.render_template("following.html", **context)
