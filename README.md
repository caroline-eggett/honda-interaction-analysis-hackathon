# V2X API Quickstart Guide
---
## Requirements
1. Make sure you have the latest version of Python installed.
    Check by running the following command in the terminal:   
    > python --version
    
    If you don't have Python 3.7.9 or greater, download the latest version on
    https://www.python.org/
    
2. Make sure you have the latest version of pip installed.
    Check by running the following command in the terminal:
    > python -m pip --version

    If you don't have the latest version run the following in the terminal:
    > python -m pip install --upgrade pip 
---
## Install the SDK package
1. Extract all files into a folder that you can access
2. Open your terminal
3. Change directory into the v2x_sdk_pkg folder (setup.py should be in this directory)
4. Run the following command to install the package using pip:   
    > pip install .
    OR
    > python3 -m pip install . --user
---
## Usage example
```python
import v2x_sdk as sdk
sdk.get_auth_code(sdk.PUBLIC,sdk.LOGIN_99P)
ctx = sdk.get_context(sdk.PUBLIC,sdk.LOGIN_99P)
Enter Auth Code :
dbfce5b8-f05c-41d8-b72b-0b689ca1b2...
ctx.set_query_type(sdk.SUMMARY)
ctx.set_days(1000)
ctx.set_limit(1000)
df,err = sdk.get_dataframe(ctx)
```
1. Import the above installed v2x_sdk package.
2. Call the sdk.get_auth_code() function. This will launch a login window in a browser and prompt for a code. 
3. Call sdk.get_context() . Copy the authentication code from the browser and paste it on the command line.
4. Set the query type to the SUMMARY table
5. Set the time window to the past 30 days.
6. Set the row count limit to 10.
7. Get a Pandas dataframe from the spat table. 
---
## Download an Entire Table to a CSV
import v2x_sdk as sdk
sdk.get_auth_code(sdk.PUBLIC, sdk.LOGIN_99P)
ctx = sdk.get_context(sdk.PUBLIC, sdk.LOGIN_99P)
ctx.set_query_type(sdk.HOST)

df_temp,err = sdk.get_pagination(sdk,ctx,1000000,10000) #(sdk, ctx, amount of rows you want total, rows per query)
df_temp.to_csv (r'./export_dataframe_HOST.csv', index = False, header=True)
print(df_temp)

1. Import the above installed v2x_sdk package.
2. Call the sdk.get_auth_code() function. This will launch a login window in a browser and prompt for a code. 
3. Call sdk.get_context() . Copy the authentication code from the browser and paste it on the command line.
4. Set the query type to the HOST table
5. Call the pagination function, providing the sdk variable, context, amount of total rows you want returned, rows per query.
6. Take the pandas dataframe (data table) and save it to a csv file in the same folder.
7. Print the dataframe to confirm download is complete

## SDK Methods
### Login and initialze the context
Set the access level. Possible values are: <PUBLIC | SECRET | TOP_SECRET>. If, for example, you set this to TOP_SECRET but you have not been granted access, the subsequent data access methods will fail. Default = PUBLIC.   
The first step is to get an Authorization Code from your Identity Provider.
```python
sdk.get_auth_code(sdk.SECRET,sdk.LOGIN_99P)
ctx = sdk.get_context(sdk.SECRET,sdk.LOGIN_99P)
```
Local environments will launch a browser and load the ID provider login page. Remote environments will present a clickable link or at least print out the login URL. The get_context() function will prompt you for the code that you will copy and past from your browser. 
```python 
ctx = get_context(access_level=PUBLIC)
```
> parameters:
> - access_level: Access level. Possible values = <PUBLIC | SECRET | TOP_SECRET>
> - returns: a Context object and prompts for the Authentication Code.
> - Hang on to the ctx object. You will need it for all other SDK functions. 

### Get the query results as a JSON object
```python
json, err = get_json(ctx, query_type=None)
```
### Get the query results as a Python dictionary
```python
dict, err = get_dictionary(ctx, query_type=None)
```
### Get the results in a Pandas dataframe
```python
df, err = get_dataframe(ctx, query_type=None)
```
Note: err will be set to None unless there is an error.  
> parameters:
> - ctx: Context object created by the login() method.
> - query_type: optional type of a query. Possible constant values defined in the sdk =  <DEVICE | EVTWARN | HOST | RVBSM | SPAT | SUMMARY>. The query types generally correspond to a table name, but not always.  
## Context setup methods
The purpose of the Context object is to provide a means of preserving state between SDK function calls. With the exeception of credentials, most context properties start out with some default value. If you set a new value for a property, the change will persist until you change it again or create a new context. 
### Query Type
Get and set the string name of the query. The constructor sets it to a default value = DEVICE. Predefined value are: <DEVICE | EVTWARN | HOST | RVBSM | SPAT | SUMMARY>
```python
get_query_type()  
set_query_type(value)
```
### Limit
Get and set the integer limit on the number of returned rows. Default = 1000
```python
get_limit()  
set_limit(value)  
```
### Pagination
Set an amount of rows to be returned in total with multiple smaller queries. Provide the sdk variable, context, total rows to be returned amount, and rows per query. See download_data.py file for full example. 
```python
df,err = sdk.get_pagination(sdk,ctx,1000000,10000)
``` 
### Paging control Key
Get and set the string key value to enable paging. Take the key from the last row of a returned query. The key is a value on each returned row. 
```python
get_key()  
set_key(value) 
``` 
### Latest time boundary
Get and set the upper bound of the time window. A string formatted as yyyy-mm-dd. No default value. 
```python
get_before()  
set_before(value)  
```
### Oldest time boundary
Get and set the lower bound of the time window. A string formatted as yyyy-mm-dd. No default value.
```python
get_after()  
set_after(value)  
```
### Number of days worth of data
Get and set the integer value for the last number of days from now to request. 
```python 
get_days()  
set_days(value)  
```
### Custom query
Set a custom GraphQL query as a JSON. The query you set here will override all other query options.  
```python
ctx.set_query(value)  
```
### Print Context
Print out a summary of the settings in the context. 
```python 
print()
```
### Final query
Generate the the final GraphQL query string for the request. 
```python
get_query(query_type=None)
```
## Examples  
The following examples assume you have imported the v2x_sdk as sdk and you've created a context called ctx.  
```python
import v2x_sdk as sdk
sdk.get_auth_code()
ctx = sdk.get_context()
```
### Get a maximum of 100 records from the past 30 days from the SPAT table as a Pandas dataframe:  
```python
ctx.set_days(30)
ctx.set_limit(100)
ctx.set_query_type(sdk.SPAT)
df, err = sdk.get_dataframe(ctx)
if err is None:
    print(df)
```
### Get HOST records from Jan 2020 to Mar 2020 as a Python dictionary:  
```python
ctx.set_after("2020-01-01")
ctx.set_before("2020-03-30")
dictionary, err = sdk.get_dictionary(ctx, sdk.HOST)
if err is None:
    print(dictionary)
```
Specifying the query name (sdk.HOST) in the sdk call is in effect only for that call. Use a context set method to change values that persist between sdk calls. Except for query_type, unset any value back to default by setting it to None.  
```python
# Unset the 30 day window
ctx.set_days(None)
# Change the default query name to the SUMMARY table 
ctx.set_query_name(sdk.SUMMARY)
```

# Written by the 99P Labs Developers