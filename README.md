A client interface and sample code for Clarivate's IP Data-API (https://developer.clarivate.com/apis/ipdata-api)


# IPData-API Client

The IPData-API Client is a helper class for Clarivate's IP Data API interface for application developers.

Full Documentation for the IPData-API is available here: https://developer.clarivate.com/apis/ipdata-api 

## Project structure

* [query.py](ipdata_api/query.py) contains the IPDataClient and supporting classes which interface with IPData-API endpoints.
* [helpers.py](ipdata_api/helpers.py) contains helper functions to leverage the IPDataClient for common use cases.
* [fields_list.py](ipdata_api/fields_list.py) contains the list of fields that are currently available for IPData-API.
* **/examples** contains some showcase examples of how to use the IPData-API wrapper.


## Installing dependencies and running the project
1. create a new virtual environment and activate the environment by running `./venv.sh`
2. install all required dependencies by run `pip install --upgrade -r requirements.txt -r requirements-dev.txt`
3. simply try the example files under /examples folder by run `python exmaple_..` (working on uploading the api wrapper to PyPI to use as a package)


## Installing as standalone package
The client can be installed directly with pip or included in another project's requirements by prefixing the repo address with `git+`
```bash
# installing directly
pip install git+https://github.com/clarivate/ipdata-api-py-client

# example of use in requirements
git+https://github.com/clarivate/ipdata-api-py-client
```

The development requirements are included as an optional dependency:
```bash
pip install 'ipdata-api-client[dev] @ git+https://github.com/clarivate/ipdata-api-py-client'
```