import os
import codecs

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


setup (
    name="stock-analyser-lib", 
    version=read("VERSION").strip(),
    description="Python library to manage Database Operations.",
    keywords="Fledjling, stock, analyzer, library",
    author="Zakaria | Ilyes",
    author_email="your-email@example.com",
    url= "https://github.com/zakaria08abouchi/stock-analyser-lib",
    install_requires=read("requirements.txt").splitlines(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)