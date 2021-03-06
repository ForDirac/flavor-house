
class ServerObject(object):
  def __init__(self):
    self.app = None
    self.db = None

  def init(self):
    from flask import Flask
    app = Flask(__name__)
    self.app = app

    from . import config
    app.config.from_object(config)

    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    self.db = db

    from flask_migrate import Migrate
    Migrate(app, db)

    # google environment variable
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("./app/" + config.GCLOUD_KEY_FILE)

server = ServerObject()
