"""
Insta485 index (main) view.

URLs include:
/accounts/create/
"""
import flask
import insta485

@insta485.app.route('/accounts/edit/')
def show_edit():
    """Display edit page."""
    
    connection = insta485.model.get_db()

    context = {
        "email": email,
        "fullname": fullname,
        "username": user_url_slug,
        "profilepic": profilepic,
    }

    return flask.render_template("create.html")