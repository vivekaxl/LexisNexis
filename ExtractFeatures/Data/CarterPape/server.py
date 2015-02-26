import server_routes, admin_routes, routes
from bottle import debug, run

STATIC_FILES_PATH = "static"
HOMEPAGE_NAME = "index.html"

if __name__ == "__main__":
	debug(True)
	run(reloader=True)
