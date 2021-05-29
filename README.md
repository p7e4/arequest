# arequest ![PyPI](https://img.shields.io/pypi/v/arequest) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arequest) [![Downloads](https://pepy.tech/badge/arequest)](https://pepy.tech/project/arequest) ![PyPI - License](https://img.shields.io/pypi/l/arequest)

_arequest is an async HTTP library, with more flexible._  

  
## Warnning

**The arequest is experimental for now, please do not use for production environment.**


## Installation

`pip install arequest`  
  
*note: python3.8 or higher required.*  


## Hello, world

``` python
import asyncio
import arequest

async def main():
    r = await arequest.get("https://httpbin.org/get")
    print(r.headers)
    print(r.status_code)
    print(r.url)
    print(r.encoding)
    print(r.text)
    print(r.cookies)
    print(r.json())
    # print(r.content)

asyncio.run(main())
```

## POST

``` python
data = {"key": "value"}

r = await arequest.post("https://httpbin.org/post", data=data)

```




