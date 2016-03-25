#!/usr/bin/python
from flask import Flask, jsonify
app = Flask(__name__)

import MySQLdb, sys, os
from datetime import datetime


db = None
db_name = 'chester'
db_pass = 'mysql'
app_port = 5000
db_addr = os.getenv('SQL_SERVER_IPADDR', '10.1.1.0')
print "DB Server: {0}".format(db_addr)

def open_mysql():
	global db
	''' Opens a connection to MySQL at the given IP Address '''
	
	try:
		# Open database connection
		db = MySQLdb.connect(db_addr,"root",db_pass)
		return True
	except:
		return False

def create_db():
	''' Create a the new database '''

	try:
		sql_query = "CREATE DATABASE IF NOT EXISTS {0};".format(db_name)
		cursor = db.cursor()
		cursor.execute(sql_query)
	except:
		return False

	return True

def open_db():
	global db
	''' Opens the database at the given IP Address '''
	
	try:
		# Open database connection
		db = MySQLdb.connect(db_addr, "root", db_pass, db_name)
	except:
		return False

	return True

def close_db():
	global db
	# disconnect from server
	db.close()

def populate_db():
	''' Populate the database with some data to view later '''

	try:
		open_db()
		sql_query = "USE {0};".format(db_name)
		cursor = db.cursor()
		cursor.execute(sql_query)

		lines = ['CREATE TABLE entry (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(40), entry VARCHAR(201), entry_date DATE);',
			'INSERT INTO entry (id, entry, entry_date, name) VALUES (NULL, "We must have a first log entry.", "2006-01-10", "Bob");',
			'INSERT INTO entry (id,entry,entry_date, name) VALUES (NULL, "Hello this is some information for the DB", "2016-03-16", "Tige");',
			'INSERT INTO entry (id,entry,entry_date, name) VALUES (NULL, "It has been a while since the last log entry, so here is a new one.", "2007-10-22", "Jesse");'
			]

		# Create some data
		for line in lines:
			sql_query = line
			cursor.execute(sql_query)
			db.commit()

		close_db()
	except:
		return False

	return True

@app.route('/initialize_db')
def initialize_db():
	reply = {'status': 'OK', 'results': "The database has been created and populated with data."}

	if not open_mysql():
		return jsonify({'status': 'FAIL', 'results': "Failed to open a connection to MySQL."})

	if not create_db():
		return jsonify({'status': 'FAIL', 'results': "Failed to create the database."})

	if not open_db():
		return jsonify({'status': 'FAIL', 'results': "Failed to open the database."})

	if not populate_db():
		return jsonify({'status': 'FAIL', 'results': "Failed to populate data into the database.  Please remove it."})

	return jsonify(reply)

@app.route('/add_row')
def add_row(text, date, name):
	# Use the right database
	open_db()

	sql_query = "INSERT INTO entry (id, entry, entry_date, name) VALUES (NULL, '{0}', '{1}', '{2}');".format(text, date, name)
	cursor = db.cursor()	
	cursor.execute(sql_query)
	db.commit()

	close_db()
	return

@app.route('/show_all_records')
def show_all_records():
	''' Get all of the records and return them as a list of dictonarys'''
	myList = []
	sql_query = "SELECT * from entry;"

	try:
		open_db()
		cursor = db.cursor()
		cursor.execute(sql_query)
		data = cursor.fetchall()
		for row in data:
			entry_date = str(row[3])
			myList.append({'id':row[0], 'name':row[1], 'entry':row[2], 'date':entry_date})

		close_db()
		reply = {'status': 'OK', 'results': myList}
	except:
		reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
	
	return jsonify(reply)

@app.route('/remove_db')
def remove_db():
	''' Remove the database '''
	sql_query = "DROP DATABASE {0};".format(db_name)

	try:
		open_mysql()
		open_db()
		cursor = db.cursor()
		cursor.execute(sql_query)

		close_db()
		reply = {'status': 'OK', 'results': "Database {0} has been removed!".format(db_name)}
	except:
		reply = {'status': 'FAIL', 'results': "Unable to remove database {0}!".format(db_name)}

	return jsonify(reply)

@app.route('/')
@app.route('/index')
def index():
	html = '''
		<center>
		<BODY style="color:#00FC00" bgcolor=black><H3>You have connected to the Application Server</H3>
		'''
	html += "Python Version information:  {}".format(sys.version_info)
	html += '''
		<p>
		Current date and time for this server: 
		'''
	html += datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	html += '''
		<H3>(while waving a hand infront of your face)<br>This is not the web page you are looking for.</H3>
		<p>
		</BODY></HTML>
		'''
	return html

if __name__ == '__main__':
	app.config.update(
		DEBUG = True)

	app.run(host='0.0.0.0', port=app_port)
