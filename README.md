A client and sample code for Clarivate's IP Data API interface for application developers.


# IPData-API Client

The IPData-API Client is a helper class for Clarivate's IP Data API interface for application developers.

Full Documentation for the IPData-API is available here: https://developer.clarivate.com/apis/ipdata-api 

## Project structure

* [ipdata.py][query.py] contains the IPDataClient and supporting classes which interface with IPData-API endpoints.
* [helpers.py] contains helper functions to leverage the IPDataClient for common use cases.
* [field_list.py] contains the list of fields that are currently available for IPData-API.
* [examples] contains some showcase examples of how to use the IPData-API wrapper.


## Installing dependencies and running the project
1. create a new virtual environment and activate the environment by running `./venv.sh`
2. install all required dependencies by run `pip install --upgrade -r requirements.txt -r requirements-dev.txt`
3. simply try the exmaple files under /examples folder by run `python exmaple_..` (woking on uploading the api wrapper to PyPI to use as a package)
