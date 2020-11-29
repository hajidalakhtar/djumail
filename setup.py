from setuptools import find_packages, setup
import urllib.request
import requests



def read_requirements():

    link = "https://gist.githubusercontent.com/hajidalakhtar/73792df96238efd649b03085eccb219a/raw/eabef4d22779bed2f0d347d1e683e27ee6493b47/gistfile1.txt"
    with urllib.request.urlopen(link) as f:
    # with open("requirements.txt", "r") as req:
        content = f.read().decode(f.headers.get_content_charset())
        requirements = content.split("\n")

    return requirements


setup(
    name="djumail",
    version="1.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        djumail=djumail.djumail:main
    """,
)