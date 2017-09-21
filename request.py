# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 00:04:50 2017

@author: David Parra

Base on code from Allan W. Smith 
http://alanwsmith.com/using-the-twitter-api-without-3rd-party-libraries

The request method allows for direct interaction with the twitter API.

https://dev.twitter.com/rest/reference

"""
import base64
import json
import urllib2
import time
import datetime

def connect(consumer_key, consumer_secret):
	"""
	Returns access token from the twitter API
	:param consumer_key: consumer key for the twitter API
	:param consumer_secret: consumer secret for the twitter API
	:return list_data: json object with the tweets info
	"""
	### Get the Access Token

	bearer_token = "%s:%s" % (consumer_key, consumer_secret)
	bearer_token_64 = base64.b64encode(bearer_token)
	token_app = "application/x-www-form-urlencoded;charset=UTF-8"

	token_request = urllib2.Request("https://api.twitter.com/oauth2/token") 
	token_request.add_header("Content-Type", token_app)
	token_request.add_header("Authorization", "Basic %s" % bearer_token_64)
	token_request.data = "grant_type=client_credentials"

	token_response = urllib2.urlopen(token_request)
	token_contents = token_response.read()
	token_data = json.loads(token_contents)
	access_token = token_data["access_token"]

	return access_token

def request(consumer_key, consumer_secret, url_request):
	"""
	Returns a json object from twitter according to url_request
	:param consumer_key: consumer key for the twitter API
	:param consumer_secret: consumer secret for the twitter API
	:param url_request: type of request to process
	:return list_data: json object with the tweets info
	"""
	### Use the Access Token to make an API request

	access_token = connect(consumer_key, consumer_secret)

	list_request = urllib2.Request(url_request)
	list_request.add_header("Authorization", "Bearer %s" % access_token)

	list_response = urllib2.urlopen(list_request)
	list_contents = list_response.read()
	list_data = json.loads(list_contents)

	return list_data

def get_attr(tweets):
	"""
	Returns attributes from the list of tweets
	:param tweets: json object with the info of the tweets
	:return source, location, coordinates: Additional tweet info in array format
	"""
	source = []
	location = []
	coordinates = []
	id_ = []

	for index, item in enumerate(tweets):
		source.append(item["source"])
		id_.append(item["id"])
		location.append(item["user"]["location"])
		if item["geo"] is not None:
			coordinates.append(item["geo"]["coordinates"])
		else: 
			coordinates.append(None)
	return source, location, coordinates, id_

def get_time_limit(consumer_key, consumer_secret):
	"""
	Returns a the limit, remaining, and seconds until the API request limit
	:return limit: request limit associated with the consumer data 
	:return remaining: requests remaining associated with the consumer data 
	:return dif: seconds between current time and next reset of the API limit 
	"""
	req = request(consumer_key, consumer_secret, "https://api.twitter.com/1.1/application/rate_limit_status.json?resources=statuses")

	limit = req["resources"]["statuses"]["/statuses/lookup"]["limit"]
	remaining = req["resources"]["statuses"]["/statuses/lookup"]["remaining"]
	reset = req["resources"]["statuses"]["/statuses/lookup"]["reset"] 

	dif = reset - time.time()
	current_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	reset_time = datetime.datetime.fromtimestamp(reset).strftime('%Y-%m-%d %H:%M:%S')
	
	print("\n")
	print("***************************************")
	print("Current time: " + str(current_time))
	print("Reset time: " + str(reset_time))
	print("seconds until next reset: " + str(dif))
	print("Remaining requests: " + str(remaining))
	print("***************************************")
	print("\n")

	return {'time': dif, 'limit' : limit, 'remaining' : remaining}  



