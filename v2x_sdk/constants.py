from enum import Enum
import os

# 
# Info about the data model and API
# 

### Keycloak setup and utility functions
# Keycloak and API constants
KK_SERVER_URL_KOTO = "https://kas.kotomatic.io/auth/"
KK_CLIENT_ID_KOTO = "api-kotomatic-prod"
KK_REALM_KOTO = "kotomatic.io"
# The API gateway base URL
API_GATEWAY_KOTO = "https://api.kotomatic.io"


KK_SERVER_URL_99P = "https://kas.99plabs.io/auth/"
KK_CLIENT_ID_99P = "api-99plabs-prod"
KK_REALM_99P= "developer.99plabs.io"
API_GATEWAY_99P = "https://api.99plabs.io"

# Default API_GATEWAY
API_GATEWAY = "https://api.99plabs.io"

HEADERS = {"User-Agent":"Python SDK"}


# Flags that the SDK or client can use to detect if the python environment 
# is executing local or remote terminal or notebook
IS_LOCAL = False
IS_REMOTE = False
IS_TERMINAL = False
IS_NOTEBOOK = False

if 'JUPYTERHUB_HOST' in os.environ: 
    IS_REMOTE = True
    IS_NOTEBOOK = True
elif 'JPY_PARENT_PID' in os.environ:
    IS_LOCAL = True
    IS_NOTEBOOK = True

if 'SSH_CLIENT' in os.environ: 
    IS_REMOTE = True
else:
    IS_LOCAL = True

if 'TERM_PROGRAM' in os.environ: 
    IS_TERMINAL = True

if 'JPY_PARENT_PID' in os.environ: 
    IS_NOTEBOOK = True

# Access levels
PUBLIC = "/api-v2x-pub"
SECRET = "/api-v2x-sec"
TOP_SECRET = "/api-v2x-tsec"
#ACTIVE_LEVEL = "/api-v2x-pub"



# Endpoints
API_ENDPOINT_STATUS = "/status"
LOGIN_99P = "/login-99p"
LOGIN_KOTOMATIC = "/login-koto"
API_ENDPOINT_QUERY = "/query"

# Templates to build parts of the gql query string
QUERY_TMPLT = "{{ {query_type}({input}) {{ {fields} }}}}"
INPUT_TMPLT = "input:{{ {time_window} {limit} }}"
LIMIT_TMPLT = "next:{{ fetch:{fetch} }}"
PAGING_TMPLT = "next:{{fetch:{fetch} key:\"{key}\"}}"
TIME_WINDOW_TMPLT = "time_window:{{{before}{after}{days}}}"
BEFORE_TMPLT = " before:\"{before}\""
AFTER_TMPLT = " after:\"{after}\""
DAYS_TMPLT = " days:{days}"

#
# Device Query Type
#
DEVICE="device", "device"

#
# Spat Query Type
#
SPAT="spat", "device filedate filetimeutc localtimems intersectid laneid movementphase signalgroupid minendtime uuid key"

#
# Summary Query Type
#
SUMMARY="summary","device filedate filetimeutc utctime firmwareversionstring configsversionstring fullmediaversionstring deltamediaversionstring pluginsversionstring totalstorageondevice storageused startlocaltime endlocaltime swversionmaj swversionmin configversion startlatitude startlongitude endlatitude endlongitude startodometer endodometer numbsmtx numnormalbsmrx numshadowbsmrx numspatrx numwarnings numinforms numgnssoutages numcanoutages numintersectionencounters uuid key"

#
# Evtwarn Query Type
#
EVTWARN="evtwarn","device filedate filetimeutc localtimems psid rvbasicvehicleclass rvrandomid rvdevice alertlevel eventappid rvclass rvlatitude rvlongitude rvheading rvelevation rvspeed rvbrakestatus rvyawrate rvlongitudinalaccel rvturnsignal rveventflags rvrange rvrangerate rvlongoffset rvlatoffset hvlatitude hvlongitude hvheading hvelevation hvspeed hvbrakestatus hvyawrate hvlongitudinalaccel hvturnsignal uuid key"

#
# Host Query Type
#
HOST="host","device filedate filetimeutc localtimems latitude longitude elevation heading fixtypehvgps gpsspeed gpssemimajaxis gpssemiminaxis gpsorientsemimaj brakestatus speed yawrate longaccel throttlepospct steerangle turnsignal headlamp wiper transstate stabilitycontrolstatus absstatus traccontrolstatus closestintersectid uuid key"

#
# Rvbsm Query Type
#
RVBSM="rvbsm","device filedate filetimeutc localtimems rvdevice bsmpsid basicvehicleclass rvrandomid latitude longitude elevation heading gpsspeed brakestatus yawrate longaccel uuid key"

