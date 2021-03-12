# BytesToBits API
This is the **official** BytesToBits API. You can freely explore the API or host it for yourself as long as our name is mentioned in it and you abide by the `Apache License 2.0` terms.

## Using the API
You can use the API by visiting [api.bytestobits.dev](https://api.bytestobits.dev/). You must create an account and generate a token in order to be able to make requests on our API.

### **Python Example**
```py
"""
Basic example of how to retrieve a
random text from our API using the
'/text/' endpoint.
"""
import requests

BASE_URL = "https://api.bytestobits.dev/"
settings = {
    "headers": {
        "Authorization": "API_TOKEN"
    }
}
text = requests.get(BASE_URL + "text", **settings).text
print(text)
```

## Wrappers
You are free to create a wrapper for our API. You can later create a PR with it by editing the list below, and if approved, it will be added. We also mention our **official** API Wrappers in this list.

### **Official Wrappers**
- [Official Java Wrapper - BytesToJava](https://github.com/OpenSrcerer/BytesToJava) - By **[OpenSrcerer](https://github.com/OpenSrcerer)**
- [Official JavaScript Wrapper - BytesToBits](https://github.com/LostNuke/bytestobits) - By **[LostNuke](https://github.com/LostNuke)**

### **Unofficial Wrappers**
- [b2bapi](https://github.com/doublevcodes/b2bapi) - By **[doublevcodes](https://github.com/doublevcodes)**
- [btbpug](https://github.com/Pug234/btb.py) - By **[Pug234](https://github.com/Pug234)**