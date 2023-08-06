# Introduction 
Library for integrating Whale Wisdom and NPD data.

# Installation for Running Locally
1.	Installation Python packages

```bash
pip install npd-whale-wisdom=0.1.9
```

2.	Add WW Keys to Envionment
For running locally, you must add the Whale Wisdom shared and secret keys to Windows environemnt variables. These can be found in control pannel under properties. You can also search environment variables in the search bar. The shared key must be named "WW_SHARED_KEY" and the secret key must be named "WW_SECRET_KEY".


# Usage
1. Running Full Report Builder
Simply navigate to the project directory and run
```python
python main.py
```
You'll need to input the path to some input files. The web app hosting this code will pull these from Azure Storage.

2. Calling Whale Wisdom API
If you want to make a custom Whale Wisdom API call do the following:
```python
from WhaleWisdom.Common.py_whale_wisdom import call_api

#the input is string representation of a python dictionary
api_input = '{"command":"stock_lookup","symbol":"GOOGL"}'
api_res = call_api(api_input)
```
