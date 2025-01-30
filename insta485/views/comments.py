"""
Insta485 index (main) view.

URLs include:
/comments/?target=URL
"""
import flask
import insta485

@insta485.app.route('/comments/', methods=["POST"])
def handle_comments():
    """Display login page."""

    if "username" in flask.session:
        return flask.redirect(flask.url_for("show_index"))

    return flask.render_template("login.html")