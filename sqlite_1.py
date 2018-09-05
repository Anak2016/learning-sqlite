import sqlite3
import time
import datetime
from dateutil import parser 
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

#note:
#1. to inspect data, you must download DB browser for SQLite.
#2. chart from matplotlib is not accurate but it is displayed. (not sure why. )

#to do:
#1. fix matplotlib chart


style.use('fivethirtyeight')

conn = sqlite3.connect('tutorial.db') #connet to database (default: create new database if not exists)
c = conn.cursor() #create cursor 

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot( unix REAL, datastamp TEXT, keyword TEXT, value REAL)')

def data_entry():
	c.execute("INSERT INTO stuffToPlot VALUES(14525493345,'2016-02-22 21:34:21','Python',5)")

	conn.commit()

def dynamic_data_entry():
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	keyword = "Python"
	value = random.randrange(0,10)
	c.execute("INSERT INTO stuffToPlot (unix, datastamp, keyword, value) VALUES(?,?,?,?)", (unix, date, keyword, value))

	conn.commit()


def read_from_db():
	# c.execute('SELECT * FROM stuffToPlot WHERE unix > 1452554972')
	c.execute("SELECT value, datastamp FROM stuffToPlot WHERE value = 4")
	data = c.fetchall()
	# print(data)
	for row in data:
		print(row[0])
	#no need to commit to database because we use cursor not database.

def del_from_db():
	# c.execute('DELETE FROM stuffToPlot 	WHERE value = 8 or value = 9')
	c.execute('DELETE FROM stuffToPlot 	WHERE value = 99')
	conn.commit()


def update_from_db():
	c.execute('UPDATE stuffToPlot SET value = 99 WHERE value = 3')

	c.execute('SELECT * FROM stuffToPlot')
	data = c.fetchall()
	[print(row) for row in data ]
	conn.commit()

def graph_data():
    c.execute('SELECT datastamp, value FROM stuffToPlot')
    data = c.fetchall()

    dates = []
    values = []
    
    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    plt.plot_date(dates,values,'-')
    plt.show()


# for i in range(10):
# 	dynamic_data_entry()
# 	time.sleep(1)

# create_table()
# data_entry()
# read_from_db()
graph_data()
# del_from_db()
# update_from_db()

c.close()
conn.close()