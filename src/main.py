try:
	import os
	from flask import Flask
	from flask import redirect
	from flask import url_for
	from flask import render_template
	from flask import request
	from turbo_flask import Turbo
	import time
	import threading
except ModuleNotFoundError as e:
	print(e)

class app:
	def __init__(self):
		self = Flask(__name__)
		_dir = os.path.dirname(os.path.abspath(__file__))
		self.template_folder = os.path.join(_dir, "templates")
		self.static_folder = os.path.join(_dir, "static")
		self.debug = True
		turbo = Turbo(self)

		def update_clock():
			with self.app_context():
				while True:
					time.sleep(1)
					turbo.push(turbo.update(render_template('index.html'), target='clock'))

		@self.errorhandler(404)
		def page_not_found(e):
			return redirect(url_for("index"))

		@self.before_request
		def before_request():
			pass

		@self.before_first_request
		def first_request():
			threading.Thread(target=update_clock).start()

		@self.after_request
		def after_request(response):
			response.headers.add("Access-Control-Allow-Origin", "*")
			response.headers.add("Cache-control", "no-cache, no-store, must-revalidate")
			return response

		@self.route("/<page>", methods = ["GET"])
		def other(page):
			return redirect(url_for("index"))

		@self.route("/", methods = ["GET"])
		def slash():
			return redirect(url_for("index"))

		@self.route("/index.html", methods = ["GET"])
		def index():
			return render_template("index.html")

		@self.context_processor
		def realtime():
			import datetime
			date = datetime.datetime.now()
			return {"day":date.strftime("%d"),
			"months":date.strftime("%m"),
			"hour":date.strftime("%H"),
			"minute":date.strftime("%M"),
			"second":date.strftime("%S")}

		self.run(host="localhost", port=1000, threaded=True)

if __name__ == "__main__":
	app()
