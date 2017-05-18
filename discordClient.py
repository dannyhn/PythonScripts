import urllib.request
import json

def clientGet(url):
	return urllib.request.urlopen(url).read()

def clientPost(url, data):
	parsedData = json.dumps(data).encode('utf8')
	req = urllib.request.Request(url, data=parsedData, headers={'content-type': 'application/json'})
	urllib.request.urlopen(req)

print(clientGet("http://localhost:6565/getChannels"))

messageDTO = {"channel" : "272172570609188864", "message" : "hello world"}

clientPost("http://localhost:6565/message", messageDTO)

#curl -H "Content-Type: application/json" -X POST -d '{"message": "asd", "channel": "272172570609188864"}' localhost:6565/message