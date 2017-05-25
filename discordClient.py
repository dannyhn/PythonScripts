import urllib.request
import json
import zlib


def clientGet(url):
	req = urllib.request.Request(url, headers=getHeaders())
	return urllib.request.urlopen(req).read()

def clientPost(url, data):
	parsedData = json.dumps(data).encode('utf8')
	req = urllib.request.Request(url, data=parsedData, headers={'content-type': 'application/json'})
	urllib.request.urlopen(req)

def clientPostMessage(url, msg):
	req = urllib.request.Request(url, data=msg.toJson(), headers=getHeaders())
	return urllib.request.urlopen(req).read()

def decodeGzip(msg):
	return zlib.decompress(msg, 16+zlib.MAX_WBITS).decode("utf8")

def getHeaders():
	headers = {}
	headers["content-type"] = "application/json"
	headers["origin"] = "https://discordapp.com"
	headers["accept-encoding"] = "gzip, deflate, br"
	headers["accept-language"] = "en-US"
	headers["authority"] = "discordapp.com"
	headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.297 Chrome/53.0.2785.143 Discord/1.4.12 Safari/537.36"
	#headers["referer"] = "https://discordapp.com/channels/267715169520582657/272172570609188864" #dynamic
	headers["authorization"] = "MTYxNjM4MDUwNzMwODY4NzQ3.DAZfmQ.ie2zUmBT66LqxH--3IW1HenaL_g" #dynamic, change to change user
	return headers

def getGuilds():
	guildsUrl = "https://discordapp.com/api/v6/users/@me/guilds"
	guildsString = decodeGzip(clientGet(guildsUrl))
	guildsList = json.loads(guildsString)
	guildMapList = []
	for guild in guildsList:
		guildMapList.append(Guild(guild))
	return guildMapList

def getChannels(guild):
	channelsUrl = "https://discordapp.com/api/v6/guilds/{}/channels".format(guild.getId())
	channelString = decodeGzip(clientGet(channelsUrl))
	channelList = json.loads(channelString)
	channelMapList = []
	for channel in channelList:
		if ("last_message_id" in channel): # if text channel
			channelMapList.append(Channel(channel))
	return channelMapList

def getAuthorization(email, password):
	url = "https://discordapp.com/api/v6/auth/login"
	tokenString = decodeGzip(clientPostMessage(url, Login(email, password)))
	token = json.loads(tokenString)["token"]
	return token



#print(clientGet("http://localhost:6565/getChannels"))

#messageDTO = {"channel" : "272172570609188864", "message" : "hello world"}

#clientPost("http://localhost:6565/message", messageDTO)

#curl -H "Content-Type: application/json" -X POST -d '{"message": "asd", "channel": "315951206142967818"}' localhost:6565/message
#curl -H "Content-Type: application/json" -X POST -d '{"guild":null,"guildId":null,"user":"Danny","userId":"209171660224462859","channel":null,"channelId":null,"timestamp":1495400351359,"message":"b"}' localhost:6565/messageUser

class Login:
	def __init__(self, email, password):
		self._email = email
		self._password = password

	def toJson(self):
		loginMap = {}
		loginMap["email"] = self._email
		loginMap["password"] = self._password
		return json.dumps(loginMap).encode("utf8")

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

class Guild:

	def __init__(self, dict):
		self._owner = dict["owner"]
		self._permissions = dict["permissions"]
		self._icon = dict["icon"]
		self._id = dict["id"]
		self._name = dict["name"]
		self._channels = None

	def getId(self):
		return self._id

	def getName(self):
		return self._name

	def getChannels(self):
		if (self._channels != None):
			return self._channels
		channelsUrl = "https://discordapp.com/api/v6/guilds/{}/channels".format(self.getId())
		channelString = decodeGzip(clientGet(channelsUrl))
		channelList = json.loads(channelString)
		channelMapList = []
		for channel in channelList:
			if ("last_message_id" in channel): # if text channel
				channelMapList.append(Channel(channel))
		self._channels = channelMapList
		return self._channels

	def getChannelByName(self, name):
		for channel in self.getChannels():
			if channel.getName() == name:
				return channel



class Channel:

	def __init__(self, dict):
		self._guildId = dict["guild_id"]
		self._name = dict["name"]
		self._id = dict["id"]

	def getId(self):
		return self._id

	def getName(self):
		return self._name

	def getGuildId(self):
		return self._guildId

	def sendMessage(self, msg):
		url = "https://discordapp.com/api/v6/channels/{}/messages".format(self.getId())
		clientPostMessage(url, Message(msg, "", False))


#guild = getGuilds()[0]
#guild.getChannelByName("programming").sendMessage("does ")

#for channel in getChannels(getGuilds()[0]):
#	if channel.getName() == "general":
#		channel.sendMessage("testing")
#	print(channel.getName())
#clientPostMessage("https://discordapp.com/api/v6/channels/316728454647250944/messages", Message("newMessage", "", False))
#clientPostMessage("https://discordapp.com/api/v6/channels/272172570609188864/messages", Message("mymessage", "", False))
