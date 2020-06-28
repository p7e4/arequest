#!/usr/bin/python3
import setuptools

with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name="arequest",
    version="0.0.1",
    author="p7e4",
    author_email="p7e4@qq.com",
    description="arequest is a simple async HTTP library, with more flexible.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/p7e4/arequest",
    packages=setuptools.find_packages(),
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "chardet",
        "brotli",
    ],
)

