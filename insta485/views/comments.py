"""
Insta485 index (main) view.

URLs include:
/comments/?target=URL
"""
import flask
import insta485

@insta485.app.route('/comments/', methods=["POST"])
def handle_comments():
    """Update comments"""
    
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    """

    logname = "awdeorio"
    
