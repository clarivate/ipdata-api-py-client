import sys
sys.path.append('../')

import json
from ipdata_api.ipdata import IPDataClient

API_KEY = "CONSUMER KEY"

def example_caselaw_bool():
        client = IPDataClient(API_KEY)
        # 1. start filter section by building the first filter, and second filter that we want to combine with, using build_fltr()
        filter_one = client.build_fltr(alg="SQL", fld="EX_OFFICIO", op="EQ", val="False")
        print(filter_one.fltr)
        # [{'ALG': 'SQL', 'FIELD': 'EX_OFFICIO', 'OP': 'EQ', 'VALUE': 'False'}]
        filter_two = client.build_fltr(fld="PARTY_OPTIMIZED_NAME", op="EQ", val="GOOGLE") # "alg" is set to "SQL" by default, you can leave it blank
        print(filter_two.fltr)
        # [{'ALG': 'SQL', 'FIELD': 'PARTY_OPTIMIZED_NAME', 'OP': 'EQ', 'VALUE': 'GOOGLE'}]

        # 2. combine two filter objects with an "AND" operator, using build_fltr_combine()
        filter_combined = client.build_fltr_combine(fltr_one=filter_one, fltr_two=filter_two, bool_op="AND", flat=True)
        print(filter_combined.fltr)
        # [[{'ALG': 'SQL', 'FIELD': 'EX_OFFICIO', 'OP': 'EQ', 'VALUE': 'False'}], 'AND', [{'ALG': 'SQL', 'FIELD': 'PARTY_OPTIMIZED_NAME', 'OP': 'EQ', 'VALUE': 'GOOGLE'}]]

        #####################################
        # # if user like to have muitlple filters in the same bool queries, we can append it to the current bool query using build_fltr_combine()
        # filter_three = client.build_fltr(fld="PARTY_OPTIMIZED_NAME", op="EQ", val="MICROSOFT")
        # filter_combined = client.build_fltr_combine(fltr_one=filter_combined, fltr_two=filter_three, bool_op="AND", flat=True)
        # print(filter_combined.fltr)
        # # [[{'ALG': 'SQL', 'FIELD': 'EX_OFFICIO', 'OP': 'EQ', 'VALUE': 'False'}], 'AND', [{'ALG': 'SQL', 'FIELD': 'PARTY_OPTIMIZED_NAME', 'OP': 'EQ', 'VALUE': 'GOOGLE'}], 'AND', [{'ALG': 'SQL', 'FIELD': 'PARTY_OPTIMIZED_NAME', 'OP': 'EQ', 'VALUE': 'MICROSOFT'}]]
        #####################################

        # 3. complete the filter section by adding the constructed filter object using add_fltr_obj(), you can always reset it using reset_fltr()
        client.add_fltr_obj(filter_combined)
        print(client.fltr)
        # [[{'ALG': 'SQL', 'FIELD': 'EX_OFFICIO', 'OP': 'EQ', 'VALUE': 'False'}], 'AND', [{'ALG': 'SQL', 'FIELD': 'PARTY_OPTIMIZED_NAME', 'OP': 'EQ', 'VALUE': 'GOOGLE'}]]
        
        # 4. add field section using add_fields_list() or add_fields_alias(), you can always reset it using reset_fields(), for all available fields list 
        # refer to https://api.clarivate.com/swagger-ui/?url=https%3A%2F%2Fdeveloper.clarivate.com%2Fapis%2Fipdata-api%2Fswagger%3FforUser%3D12f5eba128b06a9bc6e3716a06e4b5e81571d7da
        client.add_fields_list(fields=[
                "DOCKET_REFERENCE",
                "DOCKET_COURT_NAME",
                "BINDER_ID", 
                "PARTY_OPTIMIZED_NAME"
            ])
        print(client.fields)
        # ['DOCKET_REFERENCE', 'DOCKET_COURT_NAME', 'BINDER_ID', 'PARTY_OPTIMIZED_NAME']
        
        # 5. add orderby section using add_orderby(), you can always reset it using reset_orderby()
        client.add_orderby(fld="BINDER_ID", order="ASC")
        print(client.orderby)
        # [{'BINDER_ID': 'ASC'}]

        # 6. after the completion of the query, use search() to run the search
        print(json.dumps(client.search(ip_type="caselaw"), indent=4))
        # The formed query is:
        # {
        # "QUERY": [
        #         [
        #         {
        #                 "ALG": "SQL",
        #                 "FIELD": "EX_OFFICIO",
        #                 "OP": "EQ",
        #                 "VALUE": "False"
        #         }
        #         ],
        #         "AND",
        #         [
        #         {
        #                 "ALG": "SQL",
        #                 "FIELD": "PARTY_OPTIMIZED_NAME",
        #                 "OP": "EQ",
        #                 "VALUE": "GOOGLE"
        #         }
        #         ]
        # ],
        # "FIELDS": [
        #         "DOCKET_REFERENCE",
        #         "DOCKET_COURT_NAME",
        #         "BINDER_ID",
        #         "PARTY_OPTIMIZED_NAME"
        # ],
        # "ORDERBY": [
        #         {
        #         "BINDER_ID": "ASC"
        #         }
        # ]
        # }

        # The return response is:
        # {
        # "result": [
        #         {
        #         "DOCKET_REFERENCE": ...,
        #         "DOCKET_COURT_NAME": ...,
        #         "BINDER_ID": ...,
        #         "PARTY_OPTIMIZED_NAME": "GOOGLE"
        #         },
        #         ...
        # ],
        # "total_count": ...
        # }
if __name__ == "__main__":
        example_caselaw_bool()