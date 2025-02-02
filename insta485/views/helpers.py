"""This is helper."""
from functools import wraps
import flask
import insta485


def login_required_redirect(view_func):
    """
    Decorate that checks if 'username' is in flask.session.

    - If not, redirect to /accounts/login/.
    - Otherwise, call the wrapped view function.
    """
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "username" not in flask.session:
            return flask.redirect("/accounts/login/")
        return view_func(*args, **kwargs)
    return wrapped_view


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
