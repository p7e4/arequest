#!/usr/bin/python3
from urllib.parse import urlsplit, urlencode
import asyncio
import zlib
import gzip
import chardet
from io import BytesIO
from collections import OrderedDict
import ssl
import json as sjson

__all__ = ["get", "post", "head", "put", "delete", "options", "patch", "raw", "__version__"]

__version__ = "v0.0.4"


async def get(url, params=None, **kwargs):

    return await request("get", url, params=params, **kwargs)

async def post(url, data=None, **kwargs):

    return await request("post", url, data=data, **kwargs)

async def head(url, **kwargs):

    return await request("head", url, **kwargs)

async def put(url, **kwargs):

    return await request("put", url, **kwargs)

async def delete(url, **kwargs):

    return await request("delete", url, **kwargs)

async def options(url, **kwargs):

    return await request("options", url, **kwargs)

async def patch(url, **kwargs):

    return await request("patch", url, **kwargs)


async def raw(url, raw):

    if (t := type(raw)) != str:
        raise TypeError("raw argument must be type str, {t} given.")

    return await request("raw", url, raw=raw)


class Response(object):
    def __init__(self):
        self.status_code = None
        self.headers = None
        self.content = None
        self.url = None
        self.encoding = None
        self.cookies = None

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    @property
    def text(self):
        return self.content.decode(self.encoding, "replace") if self.content else ""

    def json(self):
        if n:=self.text:
            return sjson.loads(n)


def trim(string, key):
    if string.startswith(key) and string.endswith(key):
        n = len(key)
        return string[n:-n]
    else:
        return string


async def request(method, url, params=None, data=None, raw=None, headers=None,
                 sslTimeout=20, cookies=None, verify=False, json=None, file=None):

    if method.lower() not in ("get", "post", "head", "put", "delete", "options", "patch", "raw"):
        raise ValueError(f"Unsupported method '{method}'")

    url = urlsplit(url)
    method = method.upper()

    _headers = OrderedDict()
    _headers["Host"] = url.netloc
    _headers["User-Agent"] = f"arequest/{__version__}"
    _headers["Accept-Encoding"] = "gzip, deflate"
    _headers["Accept"] = "*/*"
    _headers["Connection"] = "close"


    if params:
        if isinstance(params, dict):
            query = urlencode(params)
        else:
            raise TypeError("params must be dict.")

        if url.query:
            query = f"?{url.query}&{params}"
        else:
            query = f"?{params}"
    else:
        query = f"?{url.query}" if url.query else None

    if headers:
        if isinstance(headers, dict):
             _headers.update(headers)
        else:
            raise TypeError("headers argument must be a dict.")

    if cookies:
        if isinstance(cookies, dict):
            cookies = urlencode(cookies)
        elif not isinstance(cookies, str):
            raise TypeError("cookies argument must be a dict or a str.")

        _headers["Cookie"] = cookies

    if json:
        data = sjson.dumps(json, default=str)
        _headers["Content-Length"] = len(data)
        _headers["Content-Type"] = "application/json"

    elif data:
        if isinstance(data, dict):
            data = urlencode(data)
        elif not isinstance(data, str):
            raise TypeError("data argument must be a dict or a str.")

        _headers["Content-Length"] = len(data)
        _headers["Content-Type"] = "application/x-www-form-urlencoded"

    elif file:
        pass


    sendData = [f"{method} {url.path or '/'}{query or ''} HTTP/1.1"]
    for key, value in _headers.items():
        sendData.append(f"{key.title()}: {value}")
    
    if data: sendData.append("\r\n" + data)
    sendData.append("\r\n")

    sendData = "\r\n".join(sendData)

    # send request
    if url.scheme == "https":
        if not verify:
            sslTimeout = None
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        reader, writer = await asyncio.open_connection(
            url.hostname, url.port or 443, ssl=verify or context, ssl_handshake_timeout=sslTimeout)
    elif url.scheme == "http":
        reader, writer = await asyncio.open_connection(
            url.hostname, url.port or 80)
    else:
        raise ValueError("Unsupported scheme '{url.scheme}'")

    writer.write(sendData.encode())


    # response parse
    r = Response()
    headline = await reader.readline()
    if not headline:
        raise ValueError(f"no response from '{url.netloc}'")

    r.status_code = int(headline.decode().split()[1])
    r.url = url.geturl()

    r.headers = {}
    r.cookies = {}
    while line := await reader.readline():
        line = line.decode().rstrip()
        if line:
            k, v = line.split(": ", 1)
            if k == "Set-Cookie":
                c = v.split(";", 1)[0].strip().split("=")
                if len(c) == 2:
                    r.cookies[c[0]] = trim(c[1], "\"")
            else:
                r.headers[k] = v
        else:
            content = await reader.read()
            writer.close()
            break

    if not content:
        return r

    reader = BytesIO(content)

    if r.headers.get("Transfer-Encoding") == "chunked":
        content = []

        while line := reader.readline():
            line = line.decode().rstrip()

            if line == "0":
                break
            else:
                content.append(reader.read(int(line, 16)))
                reader.read(2)

        content = b"".join(content)

    elif (n := r.headers.get("Content-Length")):
        content = reader.read(int(n))

    if (t := r.headers.get("Content-Encoding")):
        if t == "gzip":
            content = gzip.decompress(content)

        elif t == "deflate":
            content = zlib.decompress(content)

        else:
            raise TypeError(f"Unsupported Content-Encoding '{t}'")

    if r.headers.get("Content-Type") and r.headers["Content-Type"].find("charset") != -1:
        r.encoding = r.headers["Content-Type"].split("charset=")[1]
    else:
        r.encoding = chardet.detect(content)["encoding"]

    r.content = content
    return r


async def main():
    r = await get("http://httpbin.org/get")
    print(r.headers)
    print(r.status_code)
    print(r.url)
    print(r.encoding)
    print(r.text)
    print(r.cookies)
    print(r.json())
    # print(r.content)


if __name__ == '__main__':
    asyncio.run(main())




