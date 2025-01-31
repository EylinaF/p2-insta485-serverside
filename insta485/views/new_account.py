"""User account management views."""
import os
import pathlib
import hashlib
import uuid
import flask
import insta485

LOGGER = flask.logging.create_logger(insta485.app)


@insta485.app.route("/accounts/", methods=["POST"])
def handle_account():
    """Handle login, logout, account creation, and account deletion."""
    operation = flask.request.form.get("operation")
    target_url = flask.request.args.get("target", "/")

    LOGGER.debug("Account operation: %s", operation)

    # Connect to database
    connection = insta485.model.get_db()

    if operation == "login":
        # Perform user login
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        if not username or not password:
            flask.abort(400)  # Missing fields

        # Query user
        cur = connection.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user is None:
            flask.abort(403)  # User not found

        # Verify hashed password
        salt, stored_hash = user["password"].split("$")[1:]
        hashed_password = hashlib.sha512((salt + password).encode("utf-8")).hexdigest()

        if hashed_password != stored_hash:
            flask.abort(403)  # Incorrect password

        # Set session cookie
        flask.session["username"] = username
        LOGGER.debug("User %s logged in successfully", username)

    elif operation == "logout":
        # Clear session
        flask.session.clear()
        LOGGER.debug("User logged out")

    elif operation == "create":
        # Create a new account
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        fullname = flask.request.form.get("fullname")
        email = flask.request.form.get("email")
        fileobj = flask.request.files.get("file")

        if not username or not password or not fullname or not email or not fileobj:
            flask.abort(400)  # Missing fields

        # Check if username already exists
        cur = connection.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            flask.abort(409)  # Conflict: Username already exists

        # Generate UUID-based filename for profile picture
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        save_path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(save_path)

        # Hash the password
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512((salt + password).encode("utf-8")).hexdigest()
        stored_password = f"sha512${salt}${hashed_password}"

        # Insert into database
        connection.execute(
            "INSERT INTO users (username, fullname, email, filename, password) VALUES (?, ?, ?, ?, ?)",
            (username, fullname, email, uuid_basename, stored_password),
        )

        # Set session
        flask.session["username"] = username
        LOGGER.debug("New user created: %s", username)

    elif operation == "delete":
        # Delete the logged-in user's account
        logname = flask.session.get("username")
        if not logname:
            flask.abort(403)  # User must be logged in

        # Get user details
        cur = connection.execute("SELECT filename FROM users WHERE username = ?", (logname,))
        user = cur.fetchone()

        if user is None:
            flask.abort(404)  # User not found

        # Delete user profile picture
        file_path = insta485.app.config["UPLOAD_FOLDER"] / user["filename"]
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete all user-related data
        connection.execute("DELETE FROM likes WHERE owner = ?", (logname,))
        connection.execute("DELETE FROM comments WHERE owner = ?", (logname,))
        connection.execute("DELETE FROM posts WHERE owner = ?", (logname,))
        connection.execute("DELETE FROM users WHERE username = ?", (logname,))

        # Clear session
        flask.session.clear()
        LOGGER.debug("User %s deleted", logname)

    else:
        flask.abort(400)  # Invalid operation

    return flask.redirect(target_url)
