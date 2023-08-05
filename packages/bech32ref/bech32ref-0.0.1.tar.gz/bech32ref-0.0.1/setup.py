import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bech32ref",
    version="0.0.1",
    description="Port of @sipa's bech32 reference implementation. Includes bech32m",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/niftynei/bech32ref",
    author="Pieter Wiulle",
    author_email="pieter@wuille.net",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bech32ref"],
    include_package_data=True,
)
