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
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")

    logname = flask.session['username']


    operation = flask.request.form.get("operation")
    target_url = flask.request.args.get("target", f"/users/{logname}/")

    LOGGER.debug("operation = %s", operation)

    connection = insta485.model.get_db()

    if operation == "create":

        if "file" not in flask.request.files or flask.request.files["file"].filename == "":
            flask.abort(400) 


        fileobj = flask.request.files["file"]
        filename = fileobj.filename


        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"


        save_path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(save_path)

        connection.execute(
            "INSERT INTO posts (filename, owner) VALUES (?, ?)",
            (uuid_basename, logname),
        )

        LOGGER.debug("Created post with filename: %s", uuid_basename)

    elif operation == "delete":
        postid = flask.request.form.get("postid")
        if not postid:
            flask.abort(400)


        cur = connection.execute(
            "SELECT filename, owner FROM posts WHERE postid = ?", (postid,)
        )
        post = cur.fetchone()

        if post is None:
            flask.abort(404)
        if post["owner"] != logname:
            flask.abort(403)


        file_path = insta485.app.config["UPLOAD_FOLDER"] / post["filename"]
        if os.path.exists(file_path):
            os.remove(file_path)


        connection.execute("DELETE FROM likes WHERE postid = ?", (postid,))
        connection.execute("DELETE FROM comments WHERE postid = ?", (postid,))
        connection.execute("DELETE FROM posts WHERE postid = ?", (postid,))

        LOGGER.debug("Deleted post %s and file %s", postid, post["filename"])

    else:
        flask.abort(400)

    return flask.redirect(target_url)
