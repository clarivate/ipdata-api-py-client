#!/usr/bin/env python3
import sys
sys.path.append('../')

import json
from ipdata_api.ipdata import IPDataClient
from ipdata_api.helpers import helper_search_party_cases, helper_retrieve_case_json, \
        get_derived_case_status, get_derived_case_type_list, get_derived_case_resolution

API_KEY = "CONSUMER KEY"

def example_search_party_cases():
        client = IPDataClient(API_KEY)
        # Enter the parties to search. View helper function for more parameter options:
        case_binder_id_list = helper_search_party_cases(client=client,
                                                        party_names=["L'OREAL%", "LOREAL%"],
                                                        operator="LIKE",
                                                        result_fields=["BINDER_ID", "PARTY_OPTIMIZED_NAME"], 
                                                        area=[],
                                                        domain_types=["PATENT"]
                                                        )
        print("\n\n")        
        print("Matching Cases:", json.dumps(case_binder_id_list, indent=4))
        
        print("\n\n")
        top_n = 3
        print("Example for retrieving documents for top %s cases returned" % top_n)
        for result in case_binder_id_list["result"][:top_n]:
            binder_id = result["BINDER_ID"]
            case_json = helper_retrieve_case_json(client=client, binder_id=binder_id)
            print("Case: %s" % binder_id)
            print("Full case details (truncated): %.300s ..." % json.dumps(case_json, indent=4))
            print("Derieved fields: Case Status - %s" % get_derived_case_status(case_json))
            print("Derieved fields: Case Type - %s" % get_derived_case_type_list(case_json))
            print("Derieved fields: Case Resolution - %s" % get_derived_case_resolution(case_json))
            print("\n")

if __name__ == "__main__":
        example_search_party_cases()
