#!/usr/bin/env python3
# -*- conding:utf-8 -*-

from flask import Flask, render_template, abort
import os, json


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.errorhandler(404)
def not_found(error):
	return render_template("404.html"), 404


@app.route('/')
def index():
	file_dir = "/Users/lijunjiang/shiyanlou/shiyanlou/new/file"
	file_list = os.listdir(file_dir)
	conter = []

	for file in file_list:
		file = os.path.join(file_dir, file)
		print(file)
		if os.path.isfile(file):
			with open(file) as f:
				try:
					data = json.loads(f.read())
					print(data)
				except Exception as e:
					print(e)
				conter.append(data)
		print(conter)
	titles = []
	for data in conter:
		try:
			title = data['title']
		except Exception as e:
			print(e)
		titles.append(title)
	print(titles)
	return render_template('index.html', titles=titles) 

	
@app.route('/file/<filename>')
def file(filename):
	file_dir = "/Users/lijunjiang/shiyanlou/shiyanlou/new/file"
	get_file = os.path.join(file_dir, filename) + ".json"
	if os.path.exists(get_file):
		with open(get_file) as f:
			try:
				data = json.loads(f.read())
			except Exception as e:
				print(e)
			
			return render_template('file.html', data=data)
	else:
		abort(404)


if __name__ == "__mail__":
	app.run()
