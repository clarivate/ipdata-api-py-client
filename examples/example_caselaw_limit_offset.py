import sys
sys.path.append('../')

import json
from ipdata_api.ipdata import IPDataClient

API_KEY = "CONSUMER KEY"

def example_caselaw_limit_offset():
        client = IPDataClient(API_KEY)
        # 1. start filter section by create the single filter query using add_fltr(), you can always reset it using reset_fltr()
        client.add_fltr(alg="SQL", fld="DOCKET_COURT_NAME", op="EQ", val="BUNDESPATENTGERICHT")
        print(client.fltr)
        # {'ALG': 'SQL', 'FIELD': 'DOCKET_COURT_NAME', 'OP': 'EQ', 'VALUE': 'BUNDESPATENTGERICHT'}

        # 2. add field section using add_fields_list() or add_fields_alias(), you can always reset it using reset_fields()
        client.add_fields_list(fields=[
                "DOCKET_REFERENCE",
                "DOCKET_COURT_NAME",
                "DOCKET_COURT_PATH",
                "DOCKET_COURT_AREA",
                "DOCKET_COURT_TYPE_ADMINISTRATIVE",
                "DOCKET_COURT_TYPE_ARBITRATION",
                "DOCKET_COURT_TYPE_JUDICIAL"
            ])
        print(client.fields)
        # ['DOCKET_REFERENCE', 'DOCKET_COURT_NAME', 'DOCKET_COURT_PATH', 'DOCKET_COURT_AREA', 'DOCKET_COURT_TYPE_ADMINISTRATIVE', 'DOCKET_COURT_TYPE_ARBITRATION', 'DOCKET_COURT_TYPE_JUDICIAL']

        # 3. add limit and offset section using add_limit_and_offset(), you can always reset it using reset_limit_and_offset()
        client.add_limit_and_offset(limit=3, offset=0)
        print(client.limit)
        print(client.offset)
        # 3
        # 0

        # 4. after the completion of the query, use search() to run the search
        print(json.dumps(client.search(ip_type="caselaw"), indent=4))
        # The formed query is:
        # {
        # "QUERY": {
        #         "ALG": "SQL",
        #         "FIELD": "DOCKET_COURT_NAME",
        #         "OP": "EQ",
        #         "VALUE": "BUNDESPATENTGERICHT"
        # },
        # "FIELDS": [
        #         "DOCKET_REFERENCE",
        #         "DOCKET_COURT_NAME",
        #         "DOCKET_COURT_PATH",
        #         "DOCKET_COURT_AREA",
        #         "DOCKET_COURT_TYPE_ADMINISTRATIVE",
        #         "DOCKET_COURT_TYPE_ARBITRATION",
        #         "DOCKET_COURT_TYPE_JUDICIAL"
        # ],
        # "LIMIT": 3,
        # "OFFSET": 0
        # }

        # The return response is:
        # {
        # "result":[
        # {
        #         "DOCKET_REFERENCE":...,
        #         "DOCKET_COURT_NAME":"BUNDESPATENTGERICHT",
        #         "DOCKET_COURT_PATH":...,
        #         "DOCKET_COURT_AREA":...,
        #         "DOCKET_COURT_TYPE_ADMINISTRATIVE":...,
        #         "DOCKET_COURT_TYPE_ARBITRATION":...,
        #         "DOCKET_COURT_TYPE_JUDICIAL":...
        # },
        # ...
        # ],
        # "total_count":...
        # }

if __name__ == "__main__":
        example_caselaw_limit_offset()