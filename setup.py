
from setuptools import find_packages, setup
import requests
import urllib



def read_requirements():
    link = "https://raw.githubusercontent.com/hajidalakhtar/djumail/main/requirements.txt?token=AGU7YEOFHEKPZM7QVYYUVV27YNJGW"
    f = urllib.request.urlopen(link)
    # with open("requirements.txt", "r") as req:
    content = f.read()
    requirements = content.split("\n")

    return requirements


setup(
    name="djumail",
    version="1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        djumail=djumail.djumail:main
    """,
)