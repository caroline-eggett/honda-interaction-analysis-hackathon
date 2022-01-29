import requests
import json
import pandas as pd
from keycloak import KeycloakOpenID,exceptions
from .constants import *
from .context import Context
import webbrowser
import boto3
import io
import os
import zipfile
import time

try:
    import IPython
except ImportError:
    pass

# How to use
# import v2x_sdk as sdk
# sdk.get_auth_code(sdk.PUBLIC)
# Copy and paste Auth Code from browser
# ctx = sdk.get_context()
# ctx.set_after("2019-06-01")
# ctx.set_before("2020-06-30")
# ctx.set_limit(75)
# df,err = sdk.get_dataframe(ctx)
# print(df)

# Configure the Keycloak client
# _keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL, client_id=KK_CLIENT_ID, realm_name=KK_REALM)

# Get a refreshed access token
def refresh(ctx):
	# Refresh token
	try:
		refresh_token = ctx.kk_client().refresh_token(ctx.get_token()['refresh_token'])
		ctx.set_token(refresh_token)
	except exceptions.KeycloakGetError:
		# refresh token expired, get new token
		new_token(ctx)

# Get a new token
def new_token(ctx):
	# Get Token
	try:
		token = ctx.kk_client().token(ctx.get_username(), ctx.get_password())
		ctx.set_token(token)
	except exceptions.KeycloakAuthenticationError as ex:
		print(ex)

# Call this function in a cell by itself to get an access code from your identity provider
# Depending on the environment, how you get the code can be different
def get_auth_code(access_level=PUBLIC, portal=LOGIN_99P):
	url = get_login_url(access_level, portal)
	message = 'Open a browser and go to: ' + url
	if IS_LOCAL:
	    # If you are running locally, launch a web browser
		print(url)
		return webbrowser.open_new(url)
	elif IS_REMOTE:
		# Remote can mean a notebook or terminal, either way we can't launch a browser
		if IS_TERMINAL:
			# Return instructions and url as text
			return message
		elif IS_NOTEBOOK:
		    # If we are in a notebook, try to render a clickable link that will launch a browser
			html = '<b><a href="' +  url + '" target="_blank">Click Here</a> to login with your Identity Provider.<br>Copy the code into your clipboard and run the get_context() function.'
			try:
				return IPython.display.HTML(html)
			except NameError:
				return html
	return url
    
# Get the login URL as a plain string 
def get_login_url(access_level=PUBLIC, portal=LOGIN_99P):
	if (portal == LOGIN_KOTOMATIC):
         return API_GATEWAY_KOTO + access_level + portal
	else:
	     return API_GATEWAY_99P + access_level + portal

# Prompt the user for an auth code and return a context object
def get_context(access_level=PUBLIC,portal=LOGIN_99P):
	# Create the Context
	ctx = Context(access_level,portal)
	# Prompt user for Auth Code
	print('Enter Auth Code : ')
	code = input()
	ctx.set_code(code)
	return ctx

# Check basic connection status
def status(ctx):
	r = requests.get(ctx.get_status_url(), headers = HEADERS)
	if r.status_code == 200:
		return r.text, None
	else:
		print("Error: ", r.status_code)
		return r.text, r.status_code

# Create the HTTP authentication header with bearer token
def auth_header(ctx):
	refresh(ctx)
	header={'Authorization': 'Bearer %s' % ctx.get_token()['access_token'], "User-Agent":"Python SDK"}
	return header

### End of Keycloak stuff
### Beginning of API access functions 
# Submit the request and return the HTTP response
def submit_request(ctx, query_type=None):
	# Check if token exists
	if ctx.is_empty_token():
		new_token(ctx)

	# API URL and auth header
	query = ctx.get_query(query_type)
	r = requests.post(ctx.get_api_url(), headers=auth_header(ctx), json=query)
	if r.status_code == 200:
		return r, None
	else:
		print("Error: ", r.status_code)
		return r, r.status_code

# Get the data response in JSON format
def get_json(ctx, query_type=None):
	r, err = submit_request(ctx, query_type)

	if err is None:
		return r.text, None
	else:
		return None, err

# Get the response in a dictionary
def get_dictionary(ctx, query_type=None):
	j, err = get_json(ctx, query_type)

	if err is None:
		d = json.loads(j)
		return d, None
	else:
		return None, err

# Get the response in a Pandas dataframe
def get_dataframe(ctx, query_type=None):
	d, err = get_dictionary(ctx, query_type)

	# if the type argument is missing, then use context value.
	if not bool(query_type):
		query_type = ctx.get_query_type()

	if err is None:
		try:
			df = pd.DataFrame.from_dict(d['data'][query_type[0]])
			return df, None
		except:
			print("Error from get dataframe")
			return None, None
	else:
		return None, err

def get_pagination(sdk, context, max_rows=10000, rows_per_query=1000):
    df_pages = []
    rows_to_collect = max_rows
    
    # get the first data framed
    sep = '=' * 100
    print(sep)
    row_limit = min([rows_to_collect, rows_per_query])
    context.set_limit(row_limit)
    query_print = context.get_query()
    print(query_print)
    df,err = sdk.get_dataframe(context)
    df_pages.append(df)
    rows_to_collect -= row_limit
    print(context.get_query())
    print(f'\nFirst Query Ran for {row_limit} rows. There are {rows_to_collect} rows left to gather')
    key = df['key'].iloc[-1]

  
    
    while rows_to_collect > 0:
        # setup custom query for next page
        row_limit = min([rows_to_collect, rows_per_query])
        context = _get_next_page_query(context, row_limit, key)
        
        # run query
        df_temp,err = sdk.get_dataframe(context)
        while err is not None:
          print(err)
          print("SLEEPING 60 SEC")
          time.sleep(60)
          print("RETRYING LAST QUERY")
          df_temp,err = sdk.get_dataframe(context)

        df_pages.append(df_temp)
        rows_to_collect -= row_limit 
        print("rows left to collect:",rows_to_collect)
        # get the last key
        try:
            if df_temp is not None:
                key = df_temp['key'].iloc[-1]
            else:
                print("key error from df_temp")
        except KeyError:
            print("last data")

    
    return pd.concat(df_pages),err

def _get_next_page_query(context, row_limit, key):
	context.set_key(key)
	context.set_limit(row_limit)
	print(context.get_query())
	return context