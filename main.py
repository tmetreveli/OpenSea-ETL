from utils import api_key

import requests
import json
url = "https://api.opensea.io/api/v2/collections?chain=ethereum"

headers = {
    "accept": "application/json",
    "x-api-key": "80d4fbebbde84d26b6f03ca28279c54c"
}

response = requests.get(url, headers=headers)
data = response.json()
print(json.dumps(data, indent=4))