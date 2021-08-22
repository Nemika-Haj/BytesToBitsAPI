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

## Self-Hosting
Everyone is free to host the API on their own servers. Before you do, there are a few steps to follow in order for the API to successfully deploy.

### 1. Create a `data` directory
Create a new folder and name it `data`.
### 2. Setup Configuration
Inside the newly created `data` directory, create a `config.json` file. Inside that, fill in the following information:
```json
{
    "mongo": "MongoURI to store data",
    "genius": "Your GeniusLyrics API Key",
    "max_requests": 20
}
```
Afterwards, create a `routes.json` and paste the following:
```json
{
    "login": {
        "rule": "/login/",
        "strict_slashes": false,
        "methods": ["GET", "POST"]
    },
    "register": {
        "rule": "/register/",
        "strict_slashes": false,
        "methods": ["GET", "POST"]
    },
    "logout": {
        "rule": "/logout/",
        "strict_slashes": false
    },
    "account": {
        "rule": "/account/",
        "strict_slashes": false,
        "methods": ["GET", "POST"]
    }
}
```
### 3. Setup Security, Limits, and Reddit
To ensure account security, create a `key.key` file inside the `data` directory. Inside it, write a series of letters, numbers, and symbols that will be used to encode the account passwords. Example: `5IYShedawAWdaSZd!fwaamIxEU42_12xbk4=`
You can also use **[Fernet](https://cryptography.io/en/latest/fernet/)** to generate a key.

Afterwards, create an `admin_accounts.json` file and use this format:
```json
[
    "admin@email.com",
    "admin@email2.com",
    "..."
]
```
And a `restricted_accounts.json` using the same format.
Admin tokens have unlimited uses to the API, while restricted ones have less.

#### 3.1 Setting up Reddit
Last file to create is `reddit_config.json`. This file will be used to fetch required information to use the reddit API. Create it, and fill in the following:
```json
{
    "client_id": "Reddit Application ID",
    "client_secret": "Reddit Application Secret",
    "user_agent": "Agent Name"
}
```

## Wrappers
You are free to create a wrapper for our API. You can later create a PR with it by editing the list below, and if approved, it will be added. We also mention our **official** API Wrappers in this list.

### **Official Wrappers**
- [Official Java Wrapper - BytesToJava](https://github.com/OpenSrcerer/BytesToJava) - By **[OpenSrcerer](https://github.com/OpenSrcerer)**
- [Official JavaScript Wrapper - BytesToBits](https://github.com/LostNuke/bytestobits) - By **[LostNuke](https://github.com/LostNuke)**

### **Unofficial Wrappers**
- [b2bapi](https://github.com/doublevcodes/b2bapi) - By **[doublevcodes](https://github.com/doublevcodes)**
- [btbpython](https://github.com/Pug234/btb.py) - By **[Pug234](https://github.com/Pug234)**
