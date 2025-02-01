"""
Insta485 followers (main) view.

URLs include:
/users/<user_url_slug>/followers/
"""
import flask
import insta485
from insta485.views.helpers import get_follow_data
from insta485.views.helpers import get_logged_in_user, NotLoggedIn

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """Display user following page."""
    try:
        logname = get_logged_in_user()
    except NotLoggedIn:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connection = insta485.model.get_db()

    followers = get_follow_data(user_url_slug, "followers")

    for follower in followers:
        follower["user_img_url"] = f"/uploads/{follower['user_img_url']}"

        cur = connection.execute(
            "SELECT 1 FROM following WHERE username1 = ? AND username2 = ?",
            (logname, follower["username"])
        )
        follower["logname_follows_username"] = cur.fetchone() is not None

    context = {
        "logname": logname,
        "username": user_url_slug,
        "followers": followers,
    }
    insta485.model.close_db(error=None)
    return flask.render_template("followers.html", **context)
