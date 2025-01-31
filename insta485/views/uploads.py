"""
Uploads.

URL is.
"""
import os
import flask
import insta485


@insta485.app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    """Serve uploaded files only to authenticated users."""
    if 'username' not in flask.session:
        flask.abort(403)

    upload_folder = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"], filename
    )

    if not os.path.exists(upload_folder):
        flask.abort(404)

    return flask.send_from_directory(
        insta485.app.config["UPLOAD_FOLDER"], filename
    )
