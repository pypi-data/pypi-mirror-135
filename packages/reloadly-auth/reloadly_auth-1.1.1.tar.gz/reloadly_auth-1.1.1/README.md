# Authentication API

The implementation is based on the [Authentication API Docs](https://developers.reloadly.com/#authentication-api).

## Usage

Create an `AuthenticationAPI` instance by providing the Application credentials details (client id & secret) from
the [dashboard](https://www.reloadly.com/developers/api-settings).

```python
from authentication.client.AuthenticationAPI import AuthenticationAPI
from core.enums.Service import Service

sample = AuthenticationAPI()
a = sample.clientCredentials(clientId="*****", clientSecret="*****" service=Service.AIRTIME_SANDBOX).getAccessToken(Service.AIRTIME_SANDBOX)
print (a)
```
