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
db = ""


def db_start():
	try:
		db_close()
	except:
		pass
	time.sleep(1)
	n = os.popen("mongod --dbpath /usr/local/db --fork --logpath /usr/local/logging.log").read()
	if (n.find("ERROR") != -1):
		f = open("conf","w")
		f.write("")	
	else:
		port = n.split("\n")[1].split(" ")[2]
		f = open("conf","w")
		f.write(str(port))
		print port


def db_close():
	f = open("conf","r")
	port = f.read()
	print "# ",port
	if (port != ""):
		n = os.system("kill "+port)



def db_query_title_count(db, title):
	cnt = db.atest.find({"title": title }).count()
	if (cnt != 0):
		return str(db.atest.find_one({"title":title})['_id']), cnt
	else:
		return "", 0


def db_filter_by_crawlertime(db):
	records = []
	for record in db.atest.find({"crawltime": {"$lt": 24}}):
		records.append(record["link"])
	return records

# sentiment calculation simulator
def sentiment_cal(list):
	return 0.5

def db_insert_article(db, entry):
	entry["crawltime"] = 1
	entry["pole"] = [sentiment_cal(entry["comments"])]
	entry["extract"] = entry["article"][:50]
	entry["extract"] += "..."
	result = db.atest.insert_one(entry).inserted_id

def db_update_article(db, entry):
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
	db.atest.update_one({"title": entry["title"]}, {"$set":dbentry})

def db_handle_json(db, filename):
	li = open(filename,"r").read().split("\n")
	for line in li:
		if (line == ""): break
		entry = json.loads(line)
		title = entry["title"]
		Oid, cnt = db_query_title_count(db, title)
		if (cnt == 0):
			db_insert_article(db, entry)
		else:
			db_update_article(db, entry)

def db_query(db, keys):
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

def db_test():
	db.atest.delete_many({})
	db_handle_json(db, "test.txt")
	db_handle_json(db,"update.txt")
	db_query(db, "cellphone")


# This is a MongoDB services package 
# designed to provide functionalities 
# for crawler and daemon_server.

if __name__=="__main__":
	# start the MongoDB service in the background
	#db_start()

	# get the service handler
	db = pymongo.MongoClient().newtest

	# A test program
	db_test()
	#db_close()
