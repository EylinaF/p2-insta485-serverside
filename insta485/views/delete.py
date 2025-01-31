"""
Insta485 index (main) view.

URLs include:
/accounts/delete/
"""
import flask
import insta485

@insta485.app.route('/accounts/delete/')
def show_delete():
    """Display delete page."""

    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']
    
    return flask.render_template("delete.html")