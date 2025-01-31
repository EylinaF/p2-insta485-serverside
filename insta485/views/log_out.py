"""
Insta485 index (main) view.

URLs include:
/accounts/logout/?target=URL
"""
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route('/accounts/logout/', methods=["POST"])
def log_out():
    """Logout and return to login."""
    flask.session.clear()
    LOGGER.debug("User logged out")
    return flask.redirect("/accounts/login/")
