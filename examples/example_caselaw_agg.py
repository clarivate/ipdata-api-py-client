import sys
sys.path.append('../')

import json
from ipdata_api.ipdata import IPDataClient

API_KEY = "CONSUMER KEY"

def example_caselaw_agg():
        client = IPDataClient(API_KEY)
        # 1. start filter section by create the single filter query using add_fltr(), you can always reset it using reset_fltr()
        client.add_fltr(alg="SQL", fld="DOCKET_COURT_NAME", op="EQ", val="BUNDESPATENTGERICHT")
        print(client.fltr)
        # {'ALG': 'SQL', 'FIELD': 'DOCKET_COURT_NAME', 'OP': 'EQ', 'VALUE': 'BUNDESPATENTGERICHT'}

        # 2. add aggregation section using add_agg(), you can always reset it using reset_agg()
        client.add_agg(func="COUNT", fld="GUID", alias="ID")
        print(client.agg)
        # [{'FUNC': 'COUNT', 'FIELD': 'GUID', 'ALIAS': 'ID'}]

        # 3. add groupby section using add_groupby(), you can always reset it using reset_groupby()
        client.add_groupby(fields=["DOCKET_COURT_TYPE_JUDICIAL"])
        print(client.groupby)
        # ['DOCKET_COURT_TYPE_JUDICIAL']

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
        # "AGG": [
        #         {
        #         "FUNC": "COUNT",
        #         "FIELD": "GUID",
        #         "ALIAS": "ID"
        #         }
        # ],
        # "GROUPBY": [
        #         "DOCKET_COURT_TYPE_JUDICIAL"
        # ],
        # "LIMIT": 3,
        # "OFFSET": 0
        # }

        # The return response is:
        # {
        # "result":[
        # {
        #         "DOCKET_COURT_TYPE_JUDICIAL":...,
        #         "ID":...,
        # },
        # ...
        # ],
        # "total_count":...
        # }

if __name__ == "__main__":
        example_caselaw_agg()