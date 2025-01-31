"""
Insta485 index (main) view.

URLs include:
/logout/?target=URL
"""
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)

@insta485.app.route('/logout/', methods=["POST"])
def log_out():
   
    """
    logout and return to login
    """
    flask.session.clear()
    LOGGER.debug("User logged out")
    return flask.redirect("/accounts/login/")
