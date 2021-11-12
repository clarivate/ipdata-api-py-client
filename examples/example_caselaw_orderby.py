import sys
sys.path.append('../')

import json
from ipdata_api.ipdata import IPDataClient

API_KEY = "CONSUMER KEY"

def example_caselaw_orderby():
        client = IPDataClient(API_KEY)
        # 1. start filter section by create the single filter query using add_fltr(), you can always reset it using reset_fltr()
        client.add_fltr(alg="SQL", fld="DOCKET_COURT_NAME", op="EQ", val="BUNDESPATENTGERICHT")
        print(client.fltr)
        # {'ALG': 'SQL', 'FIELD': 'DOCKET_COURT_NAME', 'OP': 'EQ', 'VALUE': 'BUNDESPATENTGERICHT'}

        # 2. add field section using add_fields_list() or add_fields_alias(), you can always reset it using reset_fields()
        client.add_fields_alias(fields={"DOCKET_REFERENCE":"DR",
                                "DOCKET_COURT_NAME":"DCN",
                                "BINDER_ID":"BI"})
        print(client.fields)
        # {'DOCKET_REFERENCE': 'DR', 'DOCKET_COURT_NAME': 'DCN', 'BINDER_ID': 'BI'} 

        # 3. add orderby section using add_orderby(), you can always reset it using reset_orderby()
        client.add_orderby(fld="BINDER_ID", order="ASC")
        print(client.orderby)
        # [{'BINDER_ID': 'ASC'}]

        # 4. add limit and offset section using add_limit_and_offset(), you can always reset it using reset_limit_and_offset()
        client.add_limit_and_offset(limit=3, offset=0)
        print(client.limit)
        print(client.offset)
        # 3
        # 0

        # 5. after the completion of the query, use search() to run the search
        print(json.dumps(client.search(ip_type="caselaw"), indent=4))
        # The formed query is:        
        # {
        # "QUERY": {
        #         "ALG": "SQL",
        #         "FIELD": "DOCKET_COURT_NAME",
        #         "OP": "EQ",
        #         "VALUE": "BUNDESPATENTGERICHT"
        # },
        # "FIELDS": {
        #         "DOCKET_REFERENCE": "DR",
        #         "DOCKET_COURT_NAME": "DCN",
        #         "BINDER_ID": "BI"
        # },
        # "ORDERBY": [
        #         {
        #         "BINDER_ID": "ASC"
        #         }
        # ],
        # "LIMIT": 3,
        # "OFFSET": 0
        # }


        # The return response is:
        # {
        # "result":[
        # {
        #         "DR":...,
        #         "DCN":...,
        #         "BI":...
        # },
        # ...
        # ],
        # "total_count":...
        # }
if __name__ == "__main__":
        example_caselaw_orderby()