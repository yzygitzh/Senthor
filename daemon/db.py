# Written by Jialin Liu
# encoding=utf-8
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
import socket
import os
import multiprocessing
import time
import pymongo
import json

# Start the MongoDB daemon in the background
# You should not use this function in your code

def db_start():
	try:
		db_close()
	except:
		pass
	time.sleep(0.5)
	n = os.popen("mongod --dbpath /usr/local/db --fork --logpath /usr/local/logging.log").read()
	if (n.find("ERROR") != -1):
		f = open("conf","w")
		f.write("")	
	else:
		port = n.split("\n")[1].split(" ")[2]
		f = open("conf","w")
		f.write(str(port))

# Stop the MongoDB daemon in the background
# You should not use this function in your code

def db_close():
	f = open("conf","r")
	port = f.read()
	if (port != ""):
		n = os.system("kill "+port)


# Query the MongoDB to know whether the article 
# you crawlered has been in the DB

def db_query_title_count(title):
	db = pymongo.MongoClient().newtest
	cnt = db.atest.find({"title": title }).count()
	if (cnt != 0):
		return str(db.atest.find_one({"title":title})['_id']), cnt
	else:
		return "", 0

# A sentiment calculation simulator
def sentiment_cal(list):
	return 0.5

# Creat a new entry for the new article in the MongoDB
def db_insert_article(entry):
	db = pymongo.MongoClient().newtest
	entry["crawltime"] = 1
	entry["pole"] = [sentiment_cal(entry["comments"])]
	entry["extract"] = entry["article"][:50]
	entry["extract"] += "..."
	result = db.atest.insert_one(entry).inserted_id

# Update a single article with a batch of new comments,
# and a new sentiment score and increase the crawler counter
def db_update_article(entry):
	db = pymongo.MongoClient().newtest
	dbentry = db.atest.find_one({"title":entry["title"]})
	cmt_list = dbentry["comments"]
	filter_comment = []
	for comment in entry["comments"]:
		if (comment in cmt_list): continue
		filter_comment.append(comment)
	newpos = sentiment_cal(filter_comment)
	dbentry["pole"].append(newpos)
	dbentry["crawltime"] += 1
	dbentry["comments"] = cmt_list + filter_comment
	db.atest.update_one({"title": entry["title"]}, {"$set": {"pole" : dbentry["pole"], "crawltime": dbentry["crawltime"], "comments" : dbentry["comments"]}})

# Read a batch of json from the "filename" file.
# Should be called after the crawlers finish their jobs
# and write the output JSONs into output file
def db_handle_json(filename):
	db = pymongo.MongoClient().newtest
	li = open(filename,"r").read().split("\n")
	for line in li:
		if (line == ""): break
		entry = json.loads(line)
		title = entry["title"]
		Oid, cnt = db_query_title_count(title)
		if (cnt == 0):
			db_insert_article(entry)
		else:
			db_update_article(entry)

# Query the MongoDB with a batch of keywords
# Return a string of a list of JSON as the query's result
def db_query(keys):
	db = pymongo.MongoClient().newtest
	print "Search begin..."
	if (keys == ""): return
	keys = keys.split("+")
	sstr = ""
	for thekey in keys:
		sstr += '''\"'''+thekey+'''\"'''
	records = db.atest.find({"$text":{"$search":sstr}})
	full_list = []
	for record in records:
		recordDict = {}
		recordDict["pole"] = record["pole"]
		recordDict["extract"] = record["extract"]
		recordDict["title"] = record["title"]
		recordDict["link"] = record["link"]
		recordDict["source"] = record["source"]
		recordJson = json.JSONEncoder().encode(recordDict)
		full_list.append(recordDict)
	result = json.dumps(full_list)
	print result
	print "Search done..."
	return result


#  An API for crawlers to trace all the fresh articles in the Database
def db_filter_by_crawlertime():
	db = pymongo.MongoClient().newtest
	cfox = open("../crawler/crawler_fox/inc.txt","w")
	cgaurd = open("../crawler/crawler_theguardian/inc.txt","w")
	cyahoo = open("../crawler/crawler_yahoo/inc.txt","w")

	for record in db.atest.find({"crawltime": {"$lt": 24}}):
		source = record["source"]
		print source
		if (source.find("yahoo") != -1):
			cyahoo.write(record["link"]+"\n")
		elif (source.find("gaurd") != -1):
			cgaurd.write(record["link"]+"\n")
		else:
			cfox.write(record["link"]+"\n")
	cfox.close()
	cgaurd.close()
	cyahoo.close()

def db_test():
	db = pymongo.MongoClient().newtest
	db.atest.delete_many({})
	db_handle_json("test/test1.txt")
	db_handle_json("test/test2.txt")
	print os.system("pwd")
	#db_handle_json("../daemon/crawler_yahoo_out.txt")
	db_query("cellphone")
	db_filter_by_crawlertime()


# This is a MongoDB services package 
# designed to provide functionalities 
# for crawler and daemon_server.

if __name__=="__main__":
	# *********************************
	# *********************************
	# ** Here, we are testing the    **
	# ** MongoDB independent of the  **
	# ** daemon......                **
	# *********************************
	# *********************************

	# start the MongoDB service in the background
	db_start()
	# get the service handler
	# A test program
	db_test()
	#db_close()
