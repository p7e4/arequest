#!/usr/bin/python3
# require python >= 3.8

from urllib.parse import urlsplit, urlencode
import asyncio
import zlib
import gzip
import brotli
import chardet
from io import BytesIO


__version__ = "0.0.2"

async def get(url, params=None, **kwargs):

    return await request("get", url, params=params, **kwargs)

async def post(url, data=None, **kwargs):

    return await request("post", url, data=data, **kwargs)

async def head(url, **kwargs):

    return await request("head", url, **kwargs)

# async def raw(url, raw, **kwargs):

#     if (t := type(raw)) != str:
#         raise TypeError("raw argument must be a str, {t} given.")

#     return await request("raw", url, raw=raw, **kwargs)

class Response(object):
    def __init__(self):
        self.__initialised = True

    def __repr__(self):
        return f"<Response [{self.status_code}]>"


async def request(method, url, params=None, data=None, raw=None, headers=None,
                 allow_redirects=True, cookies=None):

    if method.lower() not in ("get", "post", "head", "raw"):
        raise ValueError(f"Not supported method '{method}'")

    url = urlsplit(url)
    method = method.upper()

    _headers = {
        "Host": url.netloc,
        "User-Agent": f"arequest/{__version__}",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Connection": "close",
    }

    if params:
        if isinstance(params, dict):
            params = urlencode(params)
        else:
            raise TypeError("params argument must be a dict.")

        if url.query:
            params = f"?{url.query}&{params}"
        else:
            params = f"?{params}"
    else:
        if url.query:
            params = f"?{url.query}"

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

    if data:
        if isinstance(data, dict):
            data = urlencode(data)
        elif not isinstance(data, str):
            raise TypeError("data argument must be a dict or a str.")

        _headers["Content-Length"] = len(data)
        _headers["Content-Type"] = "application/x-www-form-urlencoded"
        # data += "\r\n"


    query = [f"{method} {url.path or '/'}{params or ''} HTTP/1.1"]
    for key, value in _headers.items():
        query.append(f"{key.title()}: {value}")

    query.append("\r\n")
    query = "\r\n".join(query)


    if url.scheme == "https":
        reader, writer = await asyncio.open_connection(
            url.hostname, url.port or 443, ssl=True)
    elif url.scheme == "http":
        reader, writer = await asyncio.open_connection(
            url.hostname, url.port or 80)
    else:
        raise ValueError("unknown scheme '{url.scheme}'")

    writer.write(query.encode())
    if data: writer.write(data.encode())

    _a = await reader.readline()
    status_code = _a.decode().split()[1]

    headers = []
    while line := await reader.readline():
        line = line.decode().rstrip()
        if line:
            headers.append(line.split(": ", 1))
        else:
            headers = dict(headers)
            content = await reader.read()
            writer.close()
            break


    # response parse
    r = Response()
    r.headers = headers
    r.url = url.geturl()
    r.status_code = int(status_code)

    r.cookies = {}
    if cookie := headers.get("Set-Cookie"):
        for i in cookie.split("; "):
            v = i.strip().split("=")
            if (n := len(v)) == 1:
                r.cookies[v[0]] = "true"
            elif n == 2:
                r.cookies[v[0]] = v[1]


    if not content:
        r.content = ""
        r.text = ""
        return r


    reader = BytesIO(content)

    if headers.get("Transfer-Encoding") == "chunked":
        content = []

        while line := reader.readline():
            line = line.decode().rstrip()

            if line == "0":
                break
            else:
                content.append(reader.read(int(line, 16)))
                reader.read(2)

        content = b"".join(content)

    elif (n := headers.get("Content-Length")):
        content = reader.read(int(n))

    if (t := headers.get("Content-Encoding")):
        if t == "gzip":
            content = gzip.decompress(content)

        elif t == "deflate":
            content = zlib.decompress(content)

        elif t == "bz":
            content =  brotli.decompress(content)

        else:
            raise TypeError(f"unsupport content-encoding '{t}'")


    if headers.get("Content-Type") and headers.get("Content-Type").find("charset") != -1:
        charset = headers["Content-Type"].split("charset=")[1]

    else:
        # charset = "utf-8"
        charset = chardet.detect(content)["encoding"]

    r.encoding = charset
    r.text = content.decode(charset, "replace")

    r.content = content
    return r


    
async def main():
    r = await get("https://github.com/")
    print(r.headers)
    print(r.status_code)
    print(r.url)
    print(r.encoding)
    print(r.text)
    print(r.cookies)
    # print(r.content)
    # bytes response content

if __name__ == '__main__':
    asyncio.run(main())




