# SmoothCode Auth Python
[![Tests](https://github.com/Smooth-Code-IO/smoothcode-auth-python/actions/workflows/tests.yml/badge.svg)](https://github.com/Smooth-Code-IO/smoothcode-auth-python/actions/workflows/tests.yml)

## Introduction
Python Auth Library that exposes utility functions to authenticate SmoothCode requests

## Installation
* Supported python versions
```shell
>= python3
```
* Install using
```shell
pip install smoothcode_auth
```

## Usage
This library exposes 2 methods
* `is_dashboard_request(shop)` - This method verifies if the request for accessing the dashboard is coming from `SmoothCode`
```python
from smoothcode_auth import SmoothCodeAuth

# SmoothCode sends query parameters to the URL
# shop -> Shopify Shop in the form: `test.myshopify.com`
# hmac -> HMAC of the shop signed by your App Client Secret (can be obtained from SmoothCode Dashboard in App Settings) 

SmoothCodeAuth(request_hmac, client_secret).is_dashboard_request(shop) # returns True if the request is valid
```
* `is_webhook_request(webhook_data)` - This method verifies if the webhook request is coming from `SmoothCode` 
```python
from smoothcode_auth import SmoothCodeAuth

# SmoothCode sends hmac in the Authorization Header of the request
# It is hmac of the webhook data signed by your App Client Secret

SmoothCodeAuth(request_hmac, client_secret).is_webhook_request(webhook_data) # returns True if the request is valid
```

***
