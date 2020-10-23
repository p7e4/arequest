# arequest ![PyPI](https://img.shields.io/pypi/v/arequest) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arequest) [![Downloads](https://pepy.tech/badge/arequest)](https://pepy.tech/project/arequest)
_arequest is a simple async HTTP library, with more flexible._  
  
## Installation
`pip3 install arequest`  
  
*note: python3.8 or higher is required.*  
  
## Usage
``` python
import asyncio
import arequest

async def main():
    r = await arequest.get("https://github.com")
    print(r.headers)
    print(r.status_code)
    print(r.url)
    print(r.encoding)
    print(r.text)
    print(r.cookies)
    # print(r.content)
    # bytes response content

asyncio.run(main())
```
or use `post/head` method.

### Parameters
``` python
params = {"key1": "value", "key2": "value"}

# data and cookies also accept a str, but will not auto urlencode
data = {"key": "value"}
cookies = {"key": "value"}

headers = {"referer": "test","user-agent":"test"}

r = await arequest.post("https://httpbin.org/post", params=params, data=data,
                        headers=headers, cookies=cookies)

```
  
  
  
## Warnning
**The arequest is still in the early development stage, please do not use it in the production environment.**


