"""
Insta485 index (main) view.

URLs include:
/logout/?target=URL
"""
import flask
import insta485

@insta485.app.route('/logout/', methods=["POST"])
def log_out():
   
    
    """
    logout and return to login
    """
    
    return flask.redirect("/accounts/login/")
