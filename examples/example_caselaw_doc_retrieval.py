#!/usr/bin/env python3
import sys
sys.path.append('../')

import json
from ipdata_api.ipdata import IPDataClient
from ipdata_api.helpers import helper_retrieve_case_json, get_derived_case_status, \
                        get_derived_case_type_list, get_derived_case_resolution

API_KEY = "CONSUMER KEY"

def example_search_party_cases():
        client = IPDataClient(API_KEY)
        # Enter the binder id of the documents:
        binder_id = ["611621", "611624"]
        case_json = helper_retrieve_case_json(client=client, binder_id=binder_id)
        for res in case_json["results"]:
                print("Case: %s" % list(res.keys())[0])
                print("Full case details: %.300s ..." % json.dumps(res, indent=4))
                print("Derieved fields: Case Status - %s" % get_derived_case_status(res))
                print("Derieved fields: Case Type - %s" % get_derived_case_type_list(res))
                print("Derieved fields: Case Resolution - %s" % get_derived_case_resolution(res))
                print("\n")

if __name__ == "__main__":
        example_search_party_cases()
