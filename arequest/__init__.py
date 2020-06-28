#!/usr/bin/python3
# require python >= 3.8

"""

async def main():
    r = await get("https://github.com")
    print(r.headers)
    print(r.status_code)
    print(r.url)
    print(r.encoding)
    print(r.text)
    # print(r.content)
    # bytes response content

asyncio.run(main())

"""
__title__ = 'arequest'
__description__ = 'A simple async HTTP library, with more flexible.'
__url__ = 'https://github.com/p7e4/arequest'
__author__ = 'p7e4'

from .arequest import get, post, head, __version__

