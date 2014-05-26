
import os
from flask import Flask, abort

def canonpath(path):
	path = os.path.abspath(path)
	path = os.path.normpath(path)
	return path

app = Flask(__name__)

selfdir = canonpath(os.path.dirname(__file__))
root = canonpath(os.path.join(selfdir, ".."))
selfdir = os.path.basename(selfdir)

port = 8000

@app.route("/")
def special():
	"""Special case, limitation of flask, just pass it on"""
	return handle("")

@app.route("/<path:path>")
def handle(path):
	target = os.path.join(root, path)
	target = os.path.normpath(os.path.abspath(target))
	print "target = {!r}".format(target)

	if not target.startswith(root):
		# target is outside root, they're trying to escape!
		abort(403)

	if not os.path.exists(target):
		abort(404)

	if os.path.isdir(target):
		files = os.listdir(target)
		if target == root:
			files.remove(selfdir) # exclude the outside directory
		files = [name for name in files if not name.startswith('.')] # no hidden files
		return "DIRECTORY\n" + "\n".join(files)

	with open(target) as f:
		return f.read()

if __name__ == '__main__':
	print "Starting up"
	print "root = {!r}".format(root)
	print "selfdir = {!r}".format(selfdir)
	app.run(host='0.0.0.0', port=port)
