#!/usr/bin/python

import requests
import json

def entry( site ):
	for i in range( 0 ,5 ):
		try:
			response 	= requests.get( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles/2007civicsi@gmail.com?site={0}'.format( site ) )
			parse		= json.loads( response.content )
			is_limited	= parse[ 'result' ][ 'profile' ][ 'is_limited' ]


			reenter( site, parse[ 'result' ][ 'profile' ] )
			break
		except Exception:
			continue

def reenter( site, profile ):
	profile[ 'email' ] 			= profile[ 'id' ]
	profile[ 'favorite_show' ] 	= ''

	response = requests.post( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles/2007civicsi@gmail.com', data = json.dumps( profile ) )

def create():
	data = '{ \
				"email":"blah@blah1.com", \
				"site":"hgtv", \
				"first_name":"A", \
				"last_name":"B", \
				"confirm_email":"blah@blah1.com", \
				"address1":"asdfasfasdf", \
				"city":"asfdasdf", \
				"state":"US-CA", \
				"zip":"90210", \
				"phone_number":"5555555555", \
				"gender":"F", \
				"age.birth_month":"1", \
				"age.birth_day":"1", \
				"age.birth_year":"1987", \
				"cable_provider":"Verizon FIOS", \
				"country":"US", \
				"x_channel":"m" \
			}'
	headers = {
		"Accept" : 				"application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding" : 	"gzip, deflate",
		"Accept-Language" : 	"en-US,en;q=0.8",
		"Connection" : 			"keep-alive",
		"Content-Length" : 		"409",
		"Content-Type" : 		"application/json",
		"Host" : 				"hgtv-dreamhome.promo.eprize.com",
		"Origin" : 				"https://hgtv-dreamhome.promo.eprize.com",
		"Referer" : 			"https://hgtv-dreamhome.promo.eprize.com/hgtv",
		"User-Agent" : 			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
		"X-Requested-With" : 	"XMLHttpRequest"
	}

	response = requests.post( "https://hgtv-dreamhome.promo.eprize.com/api/profiles", headers = headers, data = data, verify = False )

	print(response.status_code)



if __name__ == "__main__":
	entry( 'hgtv' )
