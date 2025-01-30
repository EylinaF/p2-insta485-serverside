"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route("/")
def show_index():
    """Display the index page with posts from the logged-in user and followed users."""
    connection = insta485.model.get_db()
    
    # Hardcoded logged-in user for now, later replace with session
    logname = "awdeorio"

    # Get posts from the logged-in user and followed users
    posts_query = """
    SELECT posts.postid, posts.filename, posts.owner, posts.created,
           users.filename AS owner_img
    FROM posts
    JOIN users ON posts.owner = users.username
    WHERE posts.owner = ?
       OR posts.owner IN (SELECT username2 FROM following WHERE username1 = ?)
    ORDER BY posts.postid DESC;
    """
    
    posts = connection.execute(posts_query, (logname, logname)).fetchall()

    # Fetch likes and comments for each post
    for post in posts:
        postid = post["postid"]
        
        # Get like count
        likes_query = "SELECT COUNT(*) AS likes FROM likes WHERE postid = ?"
        likes = connection.execute(likes_query, (postid,)).fetchone()["likes"]

        # Check if the logged-in user liked this post
        user_liked_query = "SELECT 1 FROM likes WHERE postid = ? AND owner = ?"
        user_liked = connection.execute(user_liked_query, (postid, logname)).fetchone()
        post["liked"] = bool(user_liked)

        # Get comments
        comments_query = """
        SELECT comments.commentid, comments.text, comments.owner
        FROM comments
        WHERE comments.postid = ?
        ORDER BY comments.commentid ASC;
        """
        comments = connection.execute(comments_query, (postid,)).fetchall()

        post["likes"] = likes
        post["comments"] = comments

        # Format timestamps using arrow for human-readable format
        post["human_time"] = arrow.get(post["created"]).humanize()

    return flask.render_template("index.html", logname=logname, posts=posts)
