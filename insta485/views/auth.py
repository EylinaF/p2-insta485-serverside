"""
Insta485 index (main) view.

URLs include:
/accounts/auth/
"""
import flask
import insta485

@insta485.app.route('/accounts/auth/')
def check_auth():
    """Return 200 if user is logged in, else 403."""
    if 'username' in flask.session:
        return "", 200 
    flask.abort(403)