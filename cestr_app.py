#!/usr/bin/python
from flask import Flask, send_from_directory, request
app = Flask('cestr')

import MySQLdb
db = None
db_addr = ''
app_port = ''

def open_db():
	''' Opens the database at the given IP Address and returns the db object'''
	
	try:
		# Open database connection
		db = MySQLdb.connect("172.17.0.2","root","c1","cestr" )
		return db
	except:
		return false

def close_db(db):
	# disconnect from server
	db.close()

@app.route('/show_all_records')
def show_all_records():
	db = open_db()
	''' Get all of the records and return them as a list of dictonarys'''
	myList = []

	cursor = db.cursor()
	sql_query = "SELECT * from entry;"
	cursor.execute(sql_query)

	try:
		data = cursor.fetchall()
		for row in data:
			myList.append[{'id':row[0], 'entry':row[1], 'date':row[2], 'name':row[3]}]
	except:
		# Rollback in case there is any error
		db.rollback()
		myList = false

	close_db(db)

	print myList
	return myList

@app.route('/')
@app.route('/index')
def index():

	return show_all_records()

@app.cli.command()
@app.cli.option('--test', help='mytest')
def takearg(test):
    print test

if __name__ == '__main__':
	app.config.update(
		DEBUG = True)

	   global session, tenant

	app.run(host='0.0.0.0', port=5000)
