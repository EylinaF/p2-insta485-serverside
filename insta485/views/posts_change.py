"""Create and delete posts."""
import os
import pathlib
import uuid
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route("/posts/", methods=["POST"])
def manage_posts():
    """Handle creating and deleting posts."""
    #logname = flask.session.get("username")
    logname = "awdeorio"
    if not logname:
        flask.abort(403)  # User must be logged in

    # Get form data
    operation = flask.request.form.get("operation")
    target_url = flask.request.args.get("target", f"/users/{logname}/")

    LOGGER.debug("operation = %s", operation)

    connection = insta485.model.get_db()

    if operation == "create":
        # Ensure file exists
        if "file" not in flask.request.files or flask.request.files["file"].filename == "":
            flask.abort(400)  # Bad Request if no file is uploaded

        # Get file object and filename
        fileobj = flask.request.files["file"]
        filename = fileobj.filename

        # Generate UUID-based filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save file to disk
        save_path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(save_path)

        # Insert post into the database
        connection.execute(
            "INSERT INTO posts (filename, owner) VALUES (?, ?)",
            (uuid_basename, logname),
        )

        LOGGER.debug("Created post with filename: %s", uuid_basename)

    elif operation == "delete":
        postid = flask.request.form.get("postid")
        if not postid:
            flask.abort(400)  # Missing postid

        # Check if the post exists and if the user owns it
        cur = connection.execute(
            "SELECT filename, owner FROM posts WHERE postid = ?", (postid,)
        )
        post = cur.fetchone()

        if post is None:
            flask.abort(404)  # Post not found
        if post["owner"] != logname:
            flask.abort(403)  # User does not own the post

        # Delete the image file from disk
        file_path = insta485.app.config["UPLOAD_FOLDER"] / post["filename"]
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete all related database entries
        connection.execute("DELETE FROM likes WHERE postid = ?", (postid,))
        connection.execute("DELETE FROM comments WHERE postid = ?", (postid,))
        connection.execute("DELETE FROM posts WHERE postid = ?", (postid,))

        LOGGER.debug("Deleted post %s and file %s", postid, post["filename"])

    else:
        flask.abort(400)  # Invalid operation

    return flask.redirect(target_url)
