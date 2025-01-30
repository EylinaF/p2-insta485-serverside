import os
import flask
import insta485

@insta485.app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    """Serve uploaded files only to authenticated users."""
    
    # Check if user is logged in
    #if 'username' not in flask.session:
        #flask.abort(403)  # Forbidden if not logged in

    # Construct file path
    upload_folder = os.path.join(insta485.app.config["UPLOAD_FOLDER"], filename)
    # Check if file exists
    if not os.path.exists(upload_folder):
        flask.abort(404)  # Not Found if file doesn't exist

    # Serve file
    return flask.send_from_directory(insta485.app.config["UPLOAD_FOLDER"], filename)
