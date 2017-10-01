import urllib.request
import json
import zlib
#curl 'https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid=175882837&two_factor=0' -H 'Accept: */*' -H 'Referer: https://steamcommunity.com/market/listings/578080/PLAYERUNKNOWN%27s%20Bandana' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' --compressed

GENERAL = "https://discordapp.com/api/webhooks/364134984505622538/XC9RxZRV-D4PrfHhcUY09I0n-BM5Zu0sZkPP8BL-ZVQT0EjKHoB5Oal8GOdCH0tUdXv-"
LOG = "https://discordapp.com/api/webhooks/319967654578225153/b2r9WX9B_5m6I-FJuNESPKv8DVJlffk5OMm1G6-g3rWqAOMbqHVbxCgPoFLn4ZYH0_4x"

def decodeGzip(msg):
	return zlib.decompress(msg, 16+zlib.MAX_WBITS).decode("utf8")


def sendMessageToDiscord(msg):
	if msg == "" or msg == None:
		return
	messageMap = {"content" : msg}
	jsonMsg = json.dumps(messageMap).encode("utf8")
	req = urllib.request.Request(GENERAL, data=jsonMsg, headers=getHeadersForDiscord())
	return urllib.request.urlopen(req).read()

def getBandanaPriceFromSteam():

	req = urllib.request.Request("https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid=175882837&two_factor=0", headers=getHeadersForSteam())
	return urllib.request.urlopen(req).read().decode("utf8")

def getHeadersForDiscord():
	headers = {}
	headers["content-type"] = "application/json"
	headers["origin"] = "https://discordapp.com"
	headers["accept-encoding"] = "gzip, deflate, br"
	headers["accept-language"] = "en-US"
	headers["authority"] = "discordapp.com"
	headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.297 Chrome/53.0.2785.143 Discord/1.4.12 Safari/537.36"
	return headers

def getHeadersForSteam():
	headers = {}
	headers["Accept"] = "*/*"
	headers["X-Requested-With"] = "XMLHttpRequest"
	headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
	return headers

def sendPriceToDiscord(itemData):
	lowestSellPrice = int(itemData["lowest_sell_order"])
	highestBuyPrice = int(itemData["highest_buy_order"])

	msg = "Bandana Prices\n"
	msg += "Lowest Selling Price: ${:.2f}\n".format(lowestSellPrice / 100)
	msg += "Highest Buying Price: ${:.2f}\n".format(highestBuyPrice / 100)

	sendMessageToDiscord(msg)

sendPriceToDiscord(json.loads(getBandanaPriceFromSteam()))