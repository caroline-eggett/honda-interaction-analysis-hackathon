1. Change v2x_sdk/sdk.py keycloak imports to this: 
```
from keycloak import exceptions
from keycloak.keycloak_openid import KeycloakOpenID
```

2. In v2x_sdk/context.py, get rid of custom_headers keyword argument in KeycloakOpenID constructors on lines 63, 70. Section should look like this when done: 
```
		if (self._portal == LOGIN_KOTOMATIC):
			# Configure the Keycloak client
			headers = HEADERS
			self._keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL_KOTO, client_id=KK_CLIENT_ID_KOTO,verify=True, realm_name=KK_REALM_KOTO)	
			self._api_url = API_GATEWAY_KOTO + self._access_level + API_ENDPOINT_QUERY
			self._status_url = API_GATEWAY_KOTO + self._access_level + API_ENDPOINT_STATUS
			self._token = self._keycloak_openid.token(grant_type="authorization_code", code=code, redirect_uri=self._api_url)
		else:
			# Configure the Keycloak client
			headers = HEADERS
			self._keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL_99P, client_id=KK_CLIENT_ID_99P,verify=True, realm_name=KK_REALM_99P)	
			self._api_url = API_GATEWAY_99P + self._access_level + API_ENDPOINT_QUERY
			self._status_url = API_GATEWAY_99P + self._access_level + API_ENDPOINT_STATUS
			self._token = self._keycloak_openid.token(grant_type="authorization_code", code=code, redirect_uri=self._api_url)		if (self._portal == LOGIN_KOTOMATIC):
			# Configure the Keycloak client
			headers = HEADERS
			self._keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL_KOTO, client_id=KK_CLIENT_ID_KOTO,verify=True, realm_name=KK_REALM_KOTO)	
			self._api_url = API_GATEWAY_KOTO + self._access_level + API_ENDPOINT_QUERY
			self._status_url = API_GATEWAY_KOTO + self._access_level + API_ENDPOINT_STATUS
			self._token = self._keycloak_openid.token(grant_type="authorization_code", code=code, redirect_uri=self._api_url)
		else:
			# Configure the Keycloak client
			headers = HEADERS
			self._keycloak_openid = KeycloakOpenID(server_url=KK_SERVER_URL_99P, client_id=KK_CLIENT_ID_99P,verify=True, realm_name=KK_REALM_99P)	
			self._api_url = API_GATEWAY_99P + self._access_level + API_ENDPOINT_QUERY
			self._status_url = API_GATEWAY_99P + self._access_level + API_ENDPOINT_STATUS
			self._token = self._keycloak_openid.token(grant_type="authorization_code", code=code, redirect_uri=self._api_url)

```