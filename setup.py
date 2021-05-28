#!/usr/bin/python3
import setuptools

with open("README.md") as f:
    description = f.read()

from .arequest import __version__

setuptools.setup(
    name="arequest",
    version=__version__,
    author="p7e4",
    author_email="p7e4@qq.com",
    description="arequest is an async HTTP library, with more flexible.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/p7e4/arequest",
    packages=setuptools.find_packages(),
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.8',
    install_requires=[
        "chardet",
    ],
)

