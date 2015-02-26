from bottle import route, static_file, template
from server import HOMEPAGE_NAME, STATIC_FILES_PATH

@route("/")
@route("/home") # TODO put default home route in config.yml
def serve_home():
	return static_file(HOMEPAGE_NAME, STATIC_FILES_PATH)

@route("/static")
def serve_static_sample():
	# Get sample page as string
	static_content = open("static/static.html", "r").read()
	# Insert content into shell
	return template("shell", title="Sample static page", content=static_content)

@route("/<filename:path>")
def serve_static(filename):
	return static_file(filename, STATIC_FILES_PATH)
