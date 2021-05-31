# arequest ![PyPI](https://img.shields.io/pypi/v/arequest) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arequest) ![Downloads](https://pepy.tech/badge/arequest) ![PyPI - License](https://img.shields.io/pypi/l/arequest)

_arequest is an async HTTP library, with more flexible._  


## Warnning

**The arequest is experimental for now, please do not use for production environment.**


## Installation

`pip install -U arequest`  
  
> *python3.8 or higher required.*  


## Quickstart

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


## Passing URL parameters

``` python
await arequest.get("https://httpbin.org/get", params={"test": "123"})
```


## POST

``` python
data = {"key": "value"}
await arequest.post("https://httpbin.org/post", data=data)
```

- POST JSON

``` python
data = {"key": "value"}
await arequest.post("https://httpbin.org/post", json=data)
```


## HTTP Methods

``` python
await arequest.get("https://httpbin.org/get")
await arequest.post("https://httpbin.org/post", data={"data": "test"})
await arequest.put("https://httpbin.org/put")
await arequest.delete("https://httpbin.org/delete")
await arequest.patch("https://httpbin.org/patch")
await arequest.options("https://httpbin.org/anything")
```

## Custom Headers

``` python
headers = {
    "user-agent": "test"
}
await arequest.get("https://httpbin.org/get", headers=headers)
```

> *`headers` could override any original request header, including `Host`*


## Cookies

``` python
cookies = {
    "test": "test"
}
await arequest.get("https://httpbin.org/cookies", cookies=cookies)
```


## Unverified SSL Cert

``` python
await arequest.get("https://httpbin.org/get", verify=False)
```






