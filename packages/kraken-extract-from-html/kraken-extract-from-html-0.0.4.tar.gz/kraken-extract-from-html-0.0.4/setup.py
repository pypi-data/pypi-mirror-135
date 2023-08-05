import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kraken-extract-from-html",
    version="0.0.4",
    description="Kraken Extract From HTML",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tactik8/kraken_extract_from_html2",
    author="Tactik8",
    author_email="info@tactik8.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["kraken_extract_from_html"],
    include_package_data=True,
    install_requires=['bs4', 'extruct', 'html2text', 'ioc-finder', 'w3lib', 'boilerpy3'],
    
)