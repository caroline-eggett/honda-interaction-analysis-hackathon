import v2x_sdk as sdk
sdk.get_auth_code(sdk.PUBLIC,sdk.LOGIN_99P)
ctx = sdk.get_context(sdk.PUBLIC,sdk.LOGIN_99P)
# Enter Auth Code :
# dbfce5b8-f05c-41d8-b72b-0b689ca1b2...
ctx.set_query_type(sdk.SUMMARY)
ctx.set_days(1000)
ctx.set_limit(1000)
df,err = sdk.get_dataframe(ctx)
print(df.head()); 