"""
Insta485 index (main) view.

URLs include:
/accounts/?target=URL
"""
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
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        if not username or not password:
            flask.abort(400)

        cur = connection.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user is None:
            flask.abort(403)
        
        stored_password = user["password"] 
        # Verify hashed password
        algorithm, salt, stored_hash_password = stored_password.split("$")
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()

        if password_hash != stored_hash_password:
            flask.abort(403)

        flask.session["username"] = username
        LOGGER.debug("User %s logged in successfully", username)

    elif operation == "create":
        # Create a new account
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        fullname = flask.request.form.get("fullname")
        email = flask.request.form.get("email")
        fileobj = flask.request.files.get("file")

        if not username or not password or not fullname or not email or not fileobj:
            flask.abort(400)

        # Check if username already exists
        cur = connection.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            flask.abort(409)

        # Generate UUID-based filename for profile picture
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        # Hash the password
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        connection.execute(
            "INSERT INTO users (username, fullname, email, filename, password) VALUES (?, ?, ?, ?, ?)",
            (username, fullname, email, uuid_basename, password_db_string),
        )

        flask.session["username"] = username
        LOGGER.debug("New user created: %s", username)

    elif operation == "delete":
        # Delete the logged-in user's account
        logname = flask.session.get("username")
        if not logname:
            flask.abort(403)

        cur = connection.execute("SELECT filename FROM users WHERE username = ?", (logname,))
        user = cur.fetchone()

        file_path = insta485.app.config["UPLOAD_FOLDER"] / user["filename"]
        if os.path.exists(file_path):
            os.remove(file_path)

        connection.execute("DELETE FROM likes WHERE owner = ?", (logname,))
        connection.execute("DELETE FROM comments WHERE owner = ?", (logname,))
        connection.execute("DELETE FROM posts WHERE owner = ?", (logname,))
        connection.execute("DELETE FROM users WHERE username = ?", (logname,))

        flask.session.clear()
        LOGGER.debug("User %s deleted", logname)

    elif operation == "edit_account":
        # Edit the logged-in user's account
        if 'username' not in flask.session:
            flask.abort(403)
        
        username = flask.session.get("username")
        fullname = flask.request.form.get("fullname")
        email = flask.request.form.get("email")
        fileobj = flask.request.files.get("file")

        if not fullname or not email:
            flask.abort(400)

        cur = connection.execute("SELECT filename FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if fileobj:
            filename = fileobj.filename
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix.lower()
            uuid_basename = f"{stem}{suffix}"
            path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            old_file_path = insta485.app.config["UPLOAD_FOLDER"] / user["filename"]
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            connection.execute(
                "UPDATE users SET fullname = ?, email = ?, filename = ? WHERE username = ?",
                (fullname, email, uuid_basename, username),
            )
        else:
            connection.execute(
                "UPDATE users SET fullname = ?, email = ? WHERE username = ?",
                (fullname, email, username),
            )
            
            LOGGER.debug("User %s updated their profile.", username)     
    elif operation == "update_password":
        # Update the password for the logged-in user's account
    
        if 'username' not in flask.session:
            flask.abort(403)

        username = flask.session.get("username")
        
        password = flask.request.form.get("password")
        new_password1 = flask.request.form.get("new_password1")
        new_password2 = flask.request.form.get("new_password2")

        if not password or not new_password1 or not new_password2:
            flask.abort(400)

        cur = connection.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        if user is None:
            flask.abort(403)

        stored_password = user["password"]


        # Verify hashed password
        algorithm, salt, stored_hash_password = stored_password.split("$")
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()

        if password_hash != stored_hash_password:
            flask.abort(403)

        if new_password1 != new_password2:
            flask.abort(401)
        
        new_algorithm = 'sha512'
        new_salt = uuid.uuid4().hex
        new_hash_obj = hashlib.new(new_algorithm)
        new_password_salted = new_salt + new_password1
        new_hash_obj.update(new_password_salted.encode('utf-8'))
        new_password_hash = new_hash_obj.hexdigest()
        new_password_db_string = "$".join([new_algorithm, new_salt, new_password_hash])

        connection.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password_db_string, username),
        )

        LOGGER.debug("User %s updated their password.", username)
    insta485.model.close_db(error = None)
    return flask.redirect(target_url)
