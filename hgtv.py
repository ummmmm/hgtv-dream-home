#!/usr/bin/python

import os
import sys
import json
import time
import datetime
import requests
import ConfigParser

class HGTV:
	def __init__( self, logging = False ):
		self.users 		= []
		self.logging 	= logging
		self.debug		= open( os.path.join( os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ), 'debug.log' ), 'a' )

	def __del__( self ):
		self.debug.close()

	def add( self, user ):
		self.users.append( user )

	def create( self, user ):
		month, day, year = user[ 'birthday' ].split( '/' )

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
		}

		self.log( 'Attempting to create user {email}'.format( email = user[ 'email' ] ) )
		
		response = requests.post( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles', headers = { 'Content-Type': 'application/json' }, data = json.dumps( data ) )

		if response.status_code == 409:
			self.log( 'User {email} has already been created'.format( email = user[ 'email' ] ) )
		elif response.status_code == 201:
			self.log( 'User {email} has been created'.format( email = user[ 'email' ] ) )
		else:
			self.log( 'Unrecognized response code {status_code}'.format( status_code = response.status_code ) )

	def vote( self, email, site ):
		self.log( 'Attempting to vote for user {email} on site {site}'.format( email = email, site = site ) )

		response = requests.get( 'https://hgtv-dreamhome.promo.eprize.com/api/profiles/{email}?site={site}'.format( email = email, site = site ) )

		if response.status_code == 200:
			profile = json.loads( response.content )[ 'result' ][ 'profile' ]

			if profile[ 'is_limited' ]:
				self.log( 'Failed to vote for user {email} on site {site} because is_limited was True'.format( email = email, site = site ) )
			else:
				self.log( 'Successfully voted for user {email} on site {site}'.format( email = email, site = site ) )
		else:
			self.log( 'Failed to vote for user {email} on site {site}, response code {status_code}'.format( email = email, site = site, status_code = response.status_code ) )

	def log( self, log ):
		if self.logging:
			if log is None:
				self.debug.write( os.linesep )
			else:
				timestamp = datetime.datetime.fromtimestamp( time.time() ).strftime( '%m/%d/%y:%H:%M:%S' )
				self.debug.write( '{timestamp}: {log}{separator}'.format( timestamp = timestamp, log = log, separator = os.linesep ) )

	def run( self ):
		self.log( 'Running' )
		self.log( None )

		for user in self.users:
			self.log( '{email}'.format( email = user[ 'email' ] ) )
			self.create( user )
			self.vote( user[ 'email' ], 'hgtv' )
			self.vote( user[ 'email' ], 'frontdoor' )
			self.log( None )

		self.log( None )

if __name__ == "__main__":
	config_file = os.path.join( os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ), 'users.ini' )
	config		= ConfigParser.RawConfigParser()
	config.read( config_file )

	hgtv 		= HGTV( config.getboolean( 'settings', 'log' ) )

	for section in config.sections():
		if section != 'settings':
			hgtv.add( config._sections[ section ] )

	hgtv.run()
