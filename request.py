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

def request(consumer_key, consumer_secret, url_request):
	"""
	Returns a json object from twitter according to url_request
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

	### Use the Access Token to make an API request
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

	for index, item in enumerate(tweets):
		source.append(item["source"])
		location.append(item["user"]["location"])
		if item["geo"] is not None:
			coordinates.append(item["geo"]["coordinates"])
		else: 
			coordinates.append(None)
	return source, location, coordinates
	
