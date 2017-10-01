import praw
import urllib.request
import json
import pickle
import time

redditData = pickle.load(open( "data.p", "rb" ))
red = praw.Reddit(client_id="iF_dg6i82DPkSw", client_secret="kuhmVOwmpEtDPh73IQ4g7td8N40", user_agent="Pinder by /u/MasterTactioner")

def printSubmission(submission):
	'prints a submission object'
	print()
	for field in submission.__dict__:
		print(field, "-----", submission.__dict__[field])
	print()

def sendMessageToDiscord(msg):
	if msg == "" or msg == None:
		return
	messageMap = {"content" : msg}
	jsonMsg = json.dumps(messageMap).encode("utf8")
	req = urllib.request.Request("https://discordapp.com/api/webhooks/319967654578225153/b2r9WX9B_5m6I-FJuNESPKv8DVJlffk5OMm1G6-g3rWqAOMbqHVbxCgPoFLn4ZYH0_4x", data=jsonMsg, headers=getHeaders())
	return urllib.request.urlopen(req).read()

def getHeaders():
	headers = {}
	headers["content-type"] = "application/json"
	headers["origin"] = "https://discordapp.com"
	headers["accept-encoding"] = "gzip, deflate, br"
	headers["accept-language"] = "en-US"
	headers["authority"] = "discordapp.com"
	headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.297 Chrome/53.0.2785.143 Discord/1.4.12 Safari/537.36"
	return headers

def getSubreddits():
	subreddits = ""
	for sub in redditData["subreddits"]:
		subreddits += sub + "+"
	return subreddits[:-1]

def addId(id):
	'puts string id to data'
	if not "ids" in redditData:
		redditData["ids"] = set()
	redditData["ids"].add(id)

def checkId(id):
	'returns false if id has been saved'
	if not "ids" in redditData:
		redditData["ids"] = set()
	return id in redditData["ids"]

def addData(sub):
	'adds subreddit object to data'
	dataToAdd = {"url": sub.url, 
				 "sub": sub.subreddit_name_prefixed[2:],
				 "id" : sub.id}
	if not "data" in redditData:
		redditData["data"] = set()
	if not checkId(dataToAdd["id"]):
		addId(dataToAdd["id"])
		redditData["data"].add(str(dataToAdd))

def handleSubmission(sub):
	msgToSend = ""
	print(sub.__dict__)
	if sub.domain == "i.redd.it":
		addData(sub)
		msgToSend += sub.url + "\n"
	sendMessageToDiscord(msgToSend)

subredditToSearch = getSubreddits()
#sub = red.subreddit(subredditToSearch).random()
#handleSubmission(sub)


msgToSend = ""
for sub in red.subreddit(subredditToSearch).random_rising(limit=1000):
	#printSubmission(sub)
	print(sub.__dict__)
	if sub.domain == "i.redd.it":
		addData(sub)
		msgToSend += sub.url + "\n"
	time.sleep(1)
#sendMessageToDiscord(msgToSend)


pickle.dump( redditData, open( "data.p", "wb" ) )