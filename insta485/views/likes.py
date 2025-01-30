LOGGER = flask.logging.create_logger(insta485.app)

@insta485.app.route("/likes/", methods=["POST"])
def update_likes():
  LOGGER.debug("operation = %s", flask.request.form["operation"])
  LOGGER.debug("postid = %s", flask.request.form["postid"])
  # TODO: Update the database
  # TODO: Redirect the client with flask.redirect()
  # PITFALL: Do not call render_template()