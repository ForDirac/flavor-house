from app.core import server
server.init()

from app.controllers import user, store
app = server.app
assert(app is not None)
app.register_blueprint(user.bp)
app.register_blueprint(store.bp)

if __name__ == '__main__':
  app.run(
  	'0.0.0.0',
    port=app.config['PORT'],
    debug=True,
    threaded=True
  )
