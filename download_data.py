import v2x_sdk as sdk
import pandas as pd


sdk.get_auth_code(sdk.PUBLIC, sdk.LOGIN_99P)
ctx = sdk.get_context(sdk.PUBLIC, sdk.LOGIN_99P)

# tables = {sdk.SUMMARY:[2612,"summary"],sdk.HOST:[4816389,"host"],sdk.RVBSM:[148040,"rvbsm"],
tables = {sdk.EVTWARN:[39992,"evtwarn"],sdk.SPAT:[19389,"spat"]}

for key, value in tables.items():
    ctx.set_query_type(key)
    df_temp,err = sdk.get_pagination(sdk,ctx,max_rows=value[0],rows_per_query=50000)
    df_temp.to_csv (r'./export_dataframe_'+str(value[1])+'.csv', index = False, header=True)

print("All Tables Downloaded")

