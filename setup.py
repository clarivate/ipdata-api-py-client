from setuptools import setup, find_packages

with open("requirements.txt") as reqfile:
    requirements = reqfile.readlines()

with open("requirements-dev.txt") as devfile:
    devrequirements = devfile.readlines()


description = """The IPData-API Client is a helper class for Clarivate's IP Data API interface for application developers.
Full Documentation for the IPData-API is available here: https://developer.clarivate.com/apis/ipdata-api
"""

setup(
    name="ipdata-api-client",
    version="1.0.0",
    url="https://github.com/clarivate/ipdata-api-py-client.git",
    description=description,
    packages=find_packages(),
    install_requires=requirements,
    extras_requires = {
        "dev": devrequirements,
    }
)