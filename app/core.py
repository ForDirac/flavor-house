
class ServerObject(object):
  def __init__(self):
    self.app = None
    self.db = None

  def init(self):
    from flask import Flask, request, g
    app = Flask(__name__)
    self.app = app

    from . import config
    app.config.from_object(config)

    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    self.db = db

    from flask_migrate import flask_migrate
    Migrate(app, db)

server = ServerObject()
    