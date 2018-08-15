#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, abort
import os, json, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)


class Category(db.Model):
    __talble__ = 'category'
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Category %s>' % self.name

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category_id, content):
        self.title = title
        self.created_time = created_time
        self.category_id = category_id
        self.content = content
    def __repr__(self):
        return 

#class Categry(db.Model):
#    __talble__ = categry
#    id = db.Column(db.Integer, primary_key=True)    
#    name = db.Column(db.String(80))
#
#    def __repr__(self):
#        return '<Categry %s>' % self.name


@app.route('/')
def index():
    pass
