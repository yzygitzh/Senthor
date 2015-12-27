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
from textblob import TextBlob

def LOG(File, message):
  f = open(File, "a")
  f.write("%s %s\n" % (timestr(), message))
  f.close()

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
def sentiment_cal(List):
	result = 0.0
	if (List == []):
		return 0.0
	for text in List:
		result += TextBlob(text).sentiment.polarity
		#print text, TextBlob(text).sentiment.polarity

	result /= len(List)
	return result

# Creat a new entry for the new article in the MongoDB
def db_insert_article(entry):
	db = pymongo.MongoClient().newtest
	entry["crawltime"] = 1
	entry["pole"] = [sentiment_cal(entry["comments"])]
	entry["extract"] = entry["article"][:255]
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

	l1 = len(cmt_list)
	l2 = len(filter_comment)
	if ((l1 + l2) == 0): 
		newpos = 0.0
	else:
		tmppos = sentiment_cal(filter_comment)*1.0
		newpos = (l1 * dbentry['pole'][-1] + l2 * tmppos) / (l1 + l2)

	'''
	if (filter_comment == []):
		if (dbentry["pole"] == []):
			newpos = 0.0
		else:
			newpos = dbentry["pole"][-1]
	else:
		tmp = sentiment_cal(filter_comment)
		newpos = 
	'''

	dbentry["pole"].append(newpos)
	dbentry["crawltime"] += 1
	dbentry["comments"] = cmt_list + filter_comment
	db.atest.update_one({"title": entry["title"]}, {"$set": {"pole" : dbentry["pole"], "crawltime": dbentry["crawltime"], "comments" : dbentry["comments"]}})

# Read a batch of json from the "filename" file.
# Should be called after the crawlers finish their jobs
# and write the output JSONs into output file
def db_handle_json(filename):
	db = pymongo.MongoClient().newtest
	#print "[DEBUG]: ", filename
	try:
		li = open(filename,"r").read().split("\n")
	except:
		return

	for line in li:
		if (line == ""): break
		#print line
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
	LOG("dblog.log","Search %s begin" % keys)


	if (keys == ""): return
	keys = keys.split("+")
	sstr = ""
	for thekey in keys:
		sstr += '''\"'''+thekey+'''\"'''

	LOG("dblog.log", sstr)
	records = db.atest.find({"$text":{"$search":sstr}})
	LOG("dblog.log", str(len(records)))
	full_list = []
	for record in records:
		recordDict = {}
		recordDict["pole"] = record["pole"]
		recordDict["extract"] = record["extract"]
		recordDict["title"] = record["title"]
		recordDict["link"] = record["link"]
		recordDict["source"] = record["source"]
		t = time.localtime(float(record["appeartime"]))
		recordDict["appeartime"] = [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec]
		recordJson = json.JSONEncoder().encode(recordDict)
		full_list.append(recordDict)
	result = json.dumps(full_list)
	#print result
	LOG("dblog.log", result)
	LOG("dblog.log", "Search ends")


	return result


#  An API for crawlers to trace all the fresh articles in the Database
def db_filter_by_crawlertime():
	db = pymongo.MongoClient().newtest
	cfox = open("../crawler/crawler_fox/in.txt","w")
	cgaurd = open("../crawler/crawler_theguardian/in.txt","w")
	cyahoo = open("../crawler/crawler_yahoo/in.txt","w")

	for record in db.atest.find({"crawltime": {"$lt": 24}}):
		source = record["source"]
		#print source
		if (source.find("yahoo") != -1):
			cyahoo.write(record["link"]+"\n")
		elif (source.find("gaurd") != -1):
			cgaurd.write(record["link"]+"\n")
		elif (source.find("fox") != -1):
			cfox.write(record["link"]+"\n")
		else:
			pass
	cfox.close()
	cgaurd.close()
	cyahoo.close()

def db_test():
	db = pymongo.MongoClient().newtest
	db.atest.delete_many({})
	#db_handle_json("test/test1.txt")
	#db_handle_json("test/test2.txt")
	#print os.system("pwd")
	#db_handle_json("../daemon/crawler_yahoo_out.txt")
	#db_query("Microsoft")
	#db_filter_by_crawlertime()


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
	#db_start()
	# get the service handler
	# A test program
	db_test()
	#db_close()
