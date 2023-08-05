# innocuousbook_sdk

1. [How to use](#how-to-use)

## <span id="how-to-use"> How to use </span>

1. Install
```bash
pip install innocuousbook-sdk
```

2. Import
```python
from innocuousbook-sdk import InnoucousBookSDK
```

3. Use default
> default server host: https://dashboard.innocuous.ai  
```python
# export INNOCUOUSBOOK_TOKEN=USER_TOKEN
sdk = InnocuousBookSDK()
```
4. Use the specified token
```python
token = "USER_TOKEN"
sdk = InnocuousBookSDK(token)
```

5. Use the specified server host
```python
token = "USER_TOKEN"
host = "SERVER_HOST"
sdk = InnocuousBookSDK(token, host=host)
```
