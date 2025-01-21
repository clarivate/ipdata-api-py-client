from .ipdata import IPDataClient
from datetime import datetime
from .error import UserError


def helper_search_party_cases(client, party_names=[], operator="EQ", domain_types=["PATENT"], area=[], party_role="", exofficio="False", first_action_type="", result_fields=["BINDER_ID"]):  
    ''' This is a helper function finds the cases relating to the party and returns a list of Binder IDs associated. With the Binder IDs, you can retrieve the case details using helper_retrieve_case_json()
        Note that this helper function highlights only the most commonly queried fields. For full list of queryable fields, please see documentation at https://developer.clarivate.com/apis/ipdata-api
    
        Required parameter:
        @param party_names (API field: PARTY_OPTIMIZED_NAME) - This function will search cases related to any of the party names provided in the list.          

        Optional parameters: 
        @param operator (API field: op) - String operator to use to query party_names field. 
                                     Possible values are: EQ, LT, GT, LE, GE, NE, IN, IS, CONTAINS, STARTSWITH, ENDSWITH
        @param domain_types (API fields: DOMAIN_IS_<type>) - Types of cases to search, will be converted to query DOMAIN_IS_<type>=True. 
                                                        Possible values are PATENT, TRADEMARK, DESIGN_MODEL, DOMAIN_NAME, COPYRIGHT, UNFAIR COMPETITION, OTHER
        @param area (API field: AREA) - Legal area of interest. Leaving empty defaults to any. 
                                   Possible values are EUROPE, USA, COMMONWEALTH, CHINA, BRAZIL, JAPAN, COMMONWEALTH_OF_INDEPENDENT_STATES, ASEAN, LATAM, SOUTH_KOREA, AFRICA, MIDDLE_EAST
        @param party_role (API field: PARTY_ROLE) - Leaving empty defaults to any. 
                                               Possible values are PLAINTIFF, DEFENDANT
        @param exofficio (API field: EX_OFFICIO) - Whether an IP office is acting on behalf of any of the Parties in this Legal Case. 
                                              Possible values are True or False 
        @param first_action_type (API field: FIRST_ACTION_TYPE) - Leaving emtpy defaults to any. 
                                                             Possible values are ADMINISTRATIVE_HEARINGS, OPPOSITION, EX_PARTE_REEXAMINATION_PETITION, PTO_REEXAMINATION, INTER_PARTES_REVIEW_PETITION, POST_GRANT_REVIEW_PETITION, PETITION_UNDER_TRANSITIONAL_PROGRAM, DERIVATION_PROCEEDING, INTERFERENCE, INVALIDITY_CANCELLATION, REVOCATION, INFRINGEMENT, DECLARATORY, EMPLOYEE_INVENTION, OWNERSHIP, CONTRACT, TRIAL_FOR_CORRECTION, TRIAL_FOR_SCOPE, RETRIAL, CRIMINAL_ACTION, DOMAIN_NAME_ARBITRATION, COLLECTIVE_MANAGEMENT_ORGANISATIONS, DECLARATION_OF_WELL_KNOWN_STATUS, OTHER
        @param result_fields (API query field: FIELDS) - Response fields to return, with a limit of up to 14. 
                                                    Defaults to the Binder ID, but full list of possible values of over 100 fields available in the API documentation
    '''
    if not client or not isinstance(client, IPDataClient):
        raise UserError("Please create a client from IPDataClient with valid apikey to use this helper function.")
    if party_names == []:
        raise UserError("Please specify all the possible party names to use this helper function.")
    
    # create filters for PARTY_OPTIMIZED_NAME
    filter_party_names_combined = client.build_fltr(alg="SQL", fld="PARTY_OPTIMIZED_NAME", op=operator, val=party_names[0])
    for name in party_names[1:]:
        filter_current = client.build_fltr(alg="SQL", fld="PARTY_OPTIMIZED_NAME", op=operator, val=name)
        filter_party_names_combined = client.build_fltr_combine(fltr_one=filter_party_names_combined, fltr_two=filter_current, bool_op="OR")

    # add filters for domain_types
    if domain_types != []:
        filter_domain_types_combined = client.build_fltr(alg="SQL", fld="DOMAIN_IS_{}".format(domain_types[0]), op="EQ", val="True")
        for domain in domain_types[1:]:
            filter_current = client.build_fltr(alg="SQL", fld="DOMAIN_IS_{}".format(domain), op="EQ", val="True")
            filter_domain_types_combined = client.build_fltr_combine(fltr_one=filter_domain_types_combined, fltr_two=filter_current, bool_op="OR")

    # add filters for area if has 
    if area != []:
        filter_area_combined = client.build_fltr(alg="SQL", fld="AREA", op="EQ", val=str(area[0]))
        for a in area[1:]:
            filter_current = client.build_fltr(alg="SQL",  fld="AREA", op="EQ", val=str(a))
            filter_area_combined = client.build_fltr_combine(fltr_one=filter_area_combined, fltr_two=filter_current, bool_op="OR")

    if domain_types == [] and area == []:
        filter_combined = filter_party_names_combined
    elif domain_types == []:
        filter_combined = client.build_fltr_combine(fltr_one=filter_party_names_combined, fltr_two=filter_area_combined, bool_op="AND", flat=False)
    elif area == []:
        filter_combined = client.build_fltr_combine(fltr_one=filter_party_names_combined, fltr_two=filter_domain_types_combined, bool_op="AND", flat=False)
    else:
        filter_combined = client.build_fltr_combine(fltr_one=filter_party_names_combined, fltr_two=filter_domain_types_combined, bool_op="AND", flat=False)
        filter_combined = client.build_fltr_combine(fltr_one=filter_combined, fltr_two=filter_area_combined, bool_op="AND")

    # add filters for exofficio
    filter_exofficio = client.build_fltr(alg="SQL", fld="EX_OFFICIO", op="EQ", val=str(exofficio))
    if domain_types == [] and area == []:
        filter_combined = client.build_fltr_combine(fltr_one=filter_combined, fltr_two=filter_exofficio, bool_op="AND", flat=False)
    else:
        filter_combined = client.build_fltr_combine(fltr_one=filter_combined, fltr_two=filter_exofficio, bool_op="AND")

    # add filters for party_role if has 
    if party_role:
        filter_party_role = client.build_fltr(alg="SQL", fld="PARTY_ROLE", op="EQ", val=str(party_role))
        filter_combined = client.build_fltr_combine(fltr_one=filter_combined, fltr_two=filter_party_role, bool_op="AND")
    # add filters for party_role if has 
    if first_action_type:
        filter_first_action_type = client.build_fltr(alg="SQL", fld="FIRST_ACTION_TYPE", op="EQ", val=str(first_action_type))
        filter_combined = client.build_fltr_combine(fltr_one=filter_combined, fltr_two=filter_first_action_type, bool_op="AND")

    # complete the filter section by adding the constructed filter object using add_fltr_obj(), you can always reset it using reset_fltr()
    client.add_fltr_obj(filter_combined)

    # add field section using add_fields_list() or add_fields_alias(), you can always reset it using reset_fields(), for all available fields list 
    client.add_fields_list(fields=result_fields)    

    # add orderby section using add_orderby(), you can always reset it using reset_orderby()
    client.add_orderby(fld="BINDER_ID", order="ASC")    

    return client.search(ip_type="caselaw")

def get_derived_case_status(case_json):
    ''' Case Status
        Open, Terminated
        If WITHDRAWN OR SETTLED OR CLOSED = TRUE, then case is Terminated, else Open (or undefined would be more appropriate)
    '''
    has_results = case_json.get("results", None)
    if has_results:
        cj = case_json["results"][0][list(case_json["results"][0].keys())[0]]
    else:
        cj = case_json[list(case_json.keys())[0]]
    # cj = case_json[0]
    WITHDRAWN, SETTLED, CLOSED = cj["BINDER"].get("WITHDRAWN", "False"), cj["BINDER"].get("SETTLED", "False"), cj["BINDER"].get("CLOSED", "False")
    case_status = "Open"
    if WITHDRAWN == "True" or SETTLED == "True" or CLOSED == "True":
        case_status = "Terminated"
    return case_status

def get_derived_case_type_list(case_json):
    ''' Case Type
        Patent, Trademark, Copyright, Trade Secret
        Whatever domains are true, convert them to a single field:
        DOMAIN_IS_TRADEMARK
        DOMAIN_IS_PATENT
        DOMAIN_IS_DESIGN_MODEL
        DOMAIN_IS_DOMAIN_NAME
        DOMAIN_IS_COPYRIGHT
        DOMAIN_IS_UNFAIR_COMPETITION
        DOMAIN_IS_OTHER
    '''
    has_results = case_json.get("results", None)
    if has_results:
        cj = case_json["results"][0][list(case_json["results"][0].keys())[0]]
    else:
        cj = case_json[list(case_json.keys())[0]]
    # cj = case_json[0]
    domains = cj["BINDER"].get("DOMAINS", None)
    return domains
 
def get_derived_case_resolution(case_json):
    ''' Case Resolution
        Settlement, Claimant Win, Defendant Win, among others; could be left blank for an Open case
        Apply logic to combine case status and the winner field (DOCUMENT_WINNER - [ NONE, APPLICANT, OPPONENT, BOTH ]):
           If settlement true, then case outcome = "SETTLED"
           else if withdrawal true, then case outcome = "WITHDRAWN"
           else if there is at least 1 document with document type "on the merits" with a document_winner value, take the value from the most recent of those documents (i.e. "APPLICANT WIN", "OPPONENT WIN", "NONE WIN", "BOTH WIN")
           else "UNKNOWN"
    '''
    has_results = case_json.get("results", None)
    if has_results:
        cj = case_json["results"][0][list(case_json["results"][0].keys())[0]]
    else:
        cj = case_json[list(case_json.keys())[0]]
    # cj = case_json[0]
    WITHDRAWN, SETTLED, CLOSED = cj["BINDER"].get("WITHDRAWN", "False"), cj["BINDER"].get("SETTLED", "False"), cj["BINDER"].get("CLOSED", "False")
    case_resolution = "UNKNOWN"
    if SETTLED == "True":
        case_resolution = "SETTLED"
    elif WITHDRAWN == "True":
        case_resolution = "WITHDRAWN"
    else:
        most_recent_doc_index = 0
        most_recent_date = datetime(1900, 1, 1)
        if "DOCUMENT_DATE" in cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][0]:
            most_recent_date = datetime.strptime(cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][0]["DOCUMENT_DATE"], "%Y-%m-%d")
        on_the_merits_count = 0
        for i in range(len(cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"])):
            date_cur = datetime(1900, 1, 1)
            if "DOCUMENT_DATE" in cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][i]:
                date_cur = datetime.strptime(cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][i]["DOCUMENT_DATE"], "%Y-%m-%d")
            if date_cur > most_recent_date:
                most_recent_date = date_cur
                most_recent_doc_index = i
            if "SUBTYPE" in cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][i]:
                if cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][i]["SUBTYPE"] == "ON_THE_MERITS":
                    on_the_merits_count += 1
        if on_the_merits_count > 0:
            # print(most_recent_date, most_recent_doc_index)
            # print(cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][most_recent_doc_index])
            case_resolution = cj["BINDER"]["DOCKETS"][0]["DOCUMENTS"][most_recent_doc_index].get("WINNER", "UNKNOWN")
    return case_resolution

def helper_retrieve_case_json(client, binder_id):
    res = client.get_doc(ip_type="caselaw", id=binder_id)
    if not res.get("results", None):
        raise UserError("Invalid document ids. Please check and use the correct ids.")
    return res