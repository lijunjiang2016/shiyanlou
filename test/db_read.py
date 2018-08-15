#!/usr/bin/env python3
# -*- conding:utf-8 -*-

from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='mysql://root:root@127.0.0.1/shiyanlou',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
))

db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category_id, content):
        self.title = title
        self.created_time = created_time
        self.category = category_id
        self.content = content

    def __repr__(self):
        return

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html', files=File.query.all())

@app.route('/files/<int:file_id>')
def file(file_id):
    file_item = File.query.get(file_id)
    if file_item:
        return render_template('files.html', file_item=file_item)
    
    return abort(404)
        
