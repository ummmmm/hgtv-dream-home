#!/usr/bin/python

import os
import sys
import json
import requests
import ConfigParser

class HGTV:
	def __init__( self, logging = True ):
		self.users 		= []
		self.logging 	= logging
		self.debug		= open( os.path.join( os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ), 'debug.log' ), 'w+' )

	def __del__( self ):
		self.debug.close()

	def add( self, user ):
		self.users.append( user )

	def create( self, user ):
		month, day, year = user[ 'birthday' ].split( '/' )

		headers	= {
			'Accept' 			: 'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding' 	: 'gzip, deflate',
			'Accept-Language' 	: 'en-US,en;q=0.8',
			'Content-Type' 		: 'application/json',
			'User-Agent' 		: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'X-Requested-With'	: 'XMLHttpRequest'
		}

		data = {
			'email':			user[ 'email' ],
			'site':				'hgtv',
			'first_name': 		user[ 'first_name' ],
			'last_name': 		user[ 'last_name' ],
			'confirm_email': 	user[ 'email' ],
			'address1':			user[ 'address' ],
			'city':				user[ 'city' ],
			'state':			'{country}-{state}'.format( country = user[ 'country' ], state = user[ 'state' ] ),
			'zip':				user[ 'zip' ],
			'phone_number':		user[ 'phone_number' ],
			'gender':			'M' if user[ 'gender' ] == 'Male' else 'F',
			'age.birth_month':	month,
			'age.birth_day':	day,
			'age.birth_year':	year,
			'cable_provider':	user[ 'cable_provider' ],
			'country':			user[ 'country' ],
			'x_channel':		'm'
		}

		self.log( 'Send POST request for {email}'.format( email = user[ 'email' ] ) )

		# response = requests.post( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles', headers = headers, data = json.dumps( data ) )

		# self.log( 'Response code was {status_code}'.format( status_code = response.status_code ) )

	def vote( self, email, site ):
		self.log( 'Sending GET request for {email}'.format( email = email ) )

		response = requests.get( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles/{email}?site={site}'.format( email = email, site = site ) )

		self.log( 'Response code was {status_code}'.format( status_code = response.status_code ) )

		if response.status_code != 200:
			self.log( 'Could not vote with for {email} because status code was not valid'.format( email = email ) )
			return

		parse						= json.loads( response.content )
		profile						= parse[ 'result' ][ 'profile' ]
		profile[ 'email' ] 			= profile[ 'id' ]
		profile[ 'favorite_show' ] 	= ''

		self.log( 'Sending POST request for {email}'.format( email = email ) )

		# response = requests.post( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles/{email}'.format( email = email ), data = json.dumps( profile ) )

		# self.log( 'Response code was {status_code}'.format( status_code = response.status_code ) )

	def log( self, log ):
		if self.logging:
			self.debug.write( '{log}{separator}'.format( log = log, separator = os.linesep ) )

	def run( self ):
		for user in self.users:
			self.create( user )
			self.vote( user[ 'email' ], 'hgtv' )
			self.vote( user[ 'email' ], 'frontdoor' )

if __name__ == "__main__":
	hgtv 		= HGTV()
	config		= ConfigParser.RawConfigParser()
	config_file = os.path.join( os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ), 'users.ini' )
	config.read( config_file )

	for user in config.sections():
		hgtv.add( config._sections[ user ] )

	hgtv.run()
