"""This is helper."""
import flask
import insta485


class NotLoggedIn(Exception):
    """Custom exception for unauthenticated access."""

    pass


def get_logged_in_user():
    """Check if user is logged in and return the username."""
    if 'username' not in flask.session:
        raise NotLoggedIn  # Raise an exception instead of returning a Response
    return flask.session['username']


def get_follow_data(user_url_slug, relationship):
    """Retrieve the list of users."""
    connection = insta485.model.get_db()

    # Check if user exists
    cur = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (user_url_slug,)
    )
    if cur.fetchone() is None:
        flask.abort(404)

    # Query for either following or followers
    if relationship == "following":
        query = """
            SELECT users.username, users.filename AS user_img_url
            FROM following
            JOIN users ON following.username2 = users.username
            WHERE following.username1 = ?
        """
    elif relationship == "followers":
        query = """
            SELECT users.username, users.filename AS user_img_url
            FROM following
            JOIN users ON following.username1 = users.username
            WHERE following.username2 = ?
        """
    else:
        raise ValueError("Invalid relationship type.")
    cur = connection.execute(query, (user_url_slug,))
    users = cur.fetchall()
    return users
