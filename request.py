import base64
import json
import urllib2

def request(consumer_key, consumer_secret, url_request):
	### Setup access credentials

	### Get the Access Token

	bearer_token = "%s:%s" % (consumer_key, consumer_secret)
	bearer_token_64 = base64.b64encode(bearer_token)

	token_request = urllib2.Request("https://api.twitter.com/oauth2/token") 
	token_request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
	token_request.add_header("Authorization", "Basic %s" % bearer_token_64)
	token_request.data = "grant_type=client_credentials"

	token_response = urllib2.urlopen(token_request)
	token_contents = token_response.read()
	token_data = json.loads(token_contents)
	access_token = token_data["access_token"]

	### Use the Access Token to make an API request
	timeline_request = urllib2.Request(url_request)
	timeline_request.add_header("Authorization", "Bearer %s" % access_token)

	timeline_response = urllib2.urlopen(timeline_request)
	timeline_contents = timeline_response.read()
	timeline_data = json.loads(timeline_contents)

	#print json.dumps(timeline_data, indent=2, sort_keys=True)
	return timeline_data

def get_attr(tweets):
	source = []
	location = []
	coordinates = []
	for index, item in enumerate(tweets):
		source.append(item["source"])
		location.append(item["user"]["location"])
		if item["geo"] is not None:
			coordinates.append(item["geo"]["coordinates"])
		else 
			coordinates.append(None)
	return source, location, coordinates
	
