from keycloak import KeycloakOpenID,exceptions
from .constants import *
import os
import time
import pandas as pd

# Class to contain all the necessary information to make a query
class Context():
	# Token dictionary
	_token = None

	# Query properties
	_before = None
	_after = None
	_days = None

	# Limit and paging suppert
	_DEFAULT_LIMIT = 100
	_limit = _DEFAULT_LIMIT
	_key = None

	# Access level determines which API to call. Default to public
	_access_level = PUBLIC

	#Developer Portal Version, 99p or kotomatic, defaults to 99p (LABS OR KOTOMATIC)
	_portal = LOGIN_99P
	

	# Default query type
	_query_type = DEVICE

	# Custom gql JSON supplied by the user
	_custom_query = None

	# The API URL
	_api_url = None

	# Connection status URL
	_status_url = None

	# Initialize with username and password
	def __init__(self, access_level=_access_level, portal=_portal):
		self._access_level = access_level
		self._portal = portal
		
	# Credential methods
	def kk_client(self):
		return self._keycloak_openid

	def set_token(self,value):
		self._token = value

	def get_token(self):
		return self._token

	def is_empty_token(self):
		return not bool(self._token)

	def set_code(self, code):
		if (self._portal == LOGIN_KOTOMATIC):
			# Configure the Keycloak client
			headers = HEADERS
			self._keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL_KOTO, client_id=KK_CLIENT_ID_KOTO,verify=True, realm_name=KK_REALM_KOTO, custom_headers=headers)	
			self._api_url = API_GATEWAY_KOTO + self._access_level + API_ENDPOINT_QUERY
			self._status_url = API_GATEWAY_KOTO + self._access_level + API_ENDPOINT_STATUS
			self._token = self._keycloak_openid.token(grant_type="authorization_code", code=code, redirect_uri=self._api_url)
		else:
			# Configure the Keycloak client
			headers = HEADERS
			self._keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL_99P, client_id=KK_CLIENT_ID_99P,verify=True, realm_name=KK_REALM_99P, custom_headers=headers)	
			self._api_url = API_GATEWAY_99P + self._access_level + API_ENDPOINT_QUERY
			self._status_url = API_GATEWAY_99P + self._access_level + API_ENDPOINT_STATUS
			self._token = self._keycloak_openid.token(grant_type="authorization_code", code=code, redirect_uri=self._api_url)

	# Query setup methods
	def set_query_type(self, value):
		# Don't allow None
		if value is None:
			return "None value not allowed"

		self._query_type = value
		self._custom_query = None

	def get_query_type(self):
		return self._query_type

	def get_limit(self):
		return self._limit

	def set_limit(self, value):
		if value < 1:
			self._limit = self._DEFAULT_LIMIT
		else:
			self._limit = value

	def get_key(self):
		return self._key
		
	# User must reset key to None to turn off paging
	def set_key(self, value):
		self._key = value

	def get_before(self):
		return self._before

	def set_before(self, value):
		self._before = value

	def get_after(self):
		return self._after

	def set_after(self, value):
		self._after = value

	def get_days(self):
		return self._days

	def set_days(self, value):
		if value == None or value < 0:
			self._days = 0
		else:
			self._days = value

	def get_api_url(self):
		return self._api_url

	def get_status_url(self):
		return self._status_url

	# Set a custom graphQL query
	def set_custom_query(self, value):
		if value is not None:
			# Extract query type
			query_value = value["query"]
			query_value = query_value.strip()
			query_type = ""
			for i in range(1, len(query_value)):
				if query_value[i] != "(":
					query_type += query_value[i]
				else:
					break
			query_type = query_type.strip()

			# Extract fields from query
			closed_parenthesis_index = value["query"].find(")")
			open_bracket_index = value["query"].find("{", closed_parenthesis_index)
			closed_bracket_index = value["query"].find("}", open_bracket_index)
			fields_str = value["query"][open_bracket_index+1:closed_bracket_index].strip()
			fields_list = fields_str.split()
			fields_str = " ".join(fields_list)

			self._query_type = query_type, fields_str
				
		self._custom_query = value

	# Print the current context settings and preview of query 
	def print(self):
		mylist = ["------ Current Context --------"]
		mylist.append(f'Query Type: {self._query_type[0]}')
		mylist.append(f'Token: {self._token}')

		if bool(self._custom_query):
			mylist.append(f'Custom query: {self._custom_query}')
		else:
			mylist.append(f'Before: {self._before}')
			mylist.append(f'After: {self._after}')
			mylist.append(f'Days: {self._days}')
			mylist.append(f'Limit: {self._limit}')
			mylist.append(f'Key: {self._key}')
			mylist.append(f'Access Level: {self._access_level}')
			q = self.get_query()
			mylist.append(f'Query preview: {q}')

		mystring = os.linesep.join(mylist)
		print(mystring)

	# Generate the final gql query string
	def get_query(self, query_type=None):
		# If query_type is None then either use custom or context state query_type
		if not bool(query_type):
			# If a custom query is present then use it.
			if bool(self._custom_query):
				return self._custom_query
			# If the name argument and custom query is missing, then use instance value.
			else:
				query_type = self._query_type

		# init query parts
		days = ''
		after = ''
		before = ''
		limit = ''
		time_window = ''

		# optional days
		# if self._days > 0:
		if bool(self._days):
			days = DAYS_TMPLT.format(days=self._days)

		# optional after
		if bool(self._after):
			after = AFTER_TMPLT.format(after=self._after)

		# optional before
		if bool(self._before):
			before = BEFORE_TMPLT.format(before=self._before)

		# Always set the limit
		limit = LIMIT_TMPLT.format(fetch=self._limit)

		# optional time_window
		if bool(days) or bool(after) or bool(before):
			time_window = TIME_WINDOW_TMPLT.format(before=before,after=after,days=days)

		# optional paging 
		if bool(self._key):
			# If paging, replace limit value
			limit = PAGING_TMPLT.format(fetch=self._limit,key=self._key)

		# input part of query
		input = INPUT_TMPLT.format(time_window=time_window,limit=limit)

		# Final query
		query = { "query": QUERY_TMPLT.format(query_type=query_type[0],input=input,fields=query_type[1]) }
		return query

