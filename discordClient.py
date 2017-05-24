import urllib.request
import json

def clientGet(url):
	return urllib.request.urlopen(url).read()

def clientPost(url, data):
	parsedData = json.dumps(data).encode('utf8')
	req = urllib.request.Request(url, data=parsedData, headers={'content-type': 'application/json'})
	urllib.request.urlopen(req)

def clientPostMessage(url, msg):
	req = urllib.request.Request(url, data=msg.toJson(), headers=getHeaders())
	urllib.request.urlopen(req)

def getHeaders():
	headers = {}
	headers["content-type"] = "application/json"
	headers["origin"] = "https://discordapp.com"
	headers["accept-encoding"] = "gzip, deflate, br"
	headers["accept-language"] = "en-US"
	headers["authority"] = "discordapp.com"
	headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.297 Chrome/53.0.2785.143 Discord/1.4.12 Safari/537.36"
	headers["referer"] = "https://discordapp.com/channels/267715169520582657/272172570609188864" #dynamic
	headers["authorization"] = "MjA5MTcxNjYwMjI0NDYyODU5.DAV_Nw.BjpqzTbhutbtnYskMUq1PRTCLX8" #dynamic
	return headers

#print(clientGet("http://localhost:6565/getChannels"))

#messageDTO = {"channel" : "272172570609188864", "message" : "hello world"}

#clientPost("http://localhost:6565/message", messageDTO)

#curl -H "Content-Type: application/json" -X POST -d '{"message": "asd", "channel": "315951206142967818"}' localhost:6565/message
#curl -H "Content-Type: application/json" -X POST -d '{"guild":null,"guildId":null,"user":"Danny","userId":"209171660224462859","channel":null,"channelId":null,"timestamp":1495400351359,"message":"b"}' localhost:6565/messageUser

class Message:

	def __init__(self, content, nonce, tts):
		self._content = content
		self._nonce = nonce
		self._tts = tts

	def toJson(self):
		messageMap = {}
		messageMap["content"] = self._content
		messageMap["nonce"] = self._nonce
		messageMap["tts"] = self._tts
		return json.dumps(messageMap).encode("utf8")

clientPostMessage("https://discordapp.com/api/v6/channels/272172570609188864/messages", Message("mymessage", "", False))
