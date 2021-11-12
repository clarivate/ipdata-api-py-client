from urllib.parse import urljoin
import requests
import json
from .error import AuthError, SysError, UserError
from .query import Query
from .fields_list import AVAILABLE_FIELDS

class Filter:
    """
    The Filter class is used to supporting the boolean expression of 'filter' input of IpdataAPI.
    """
    def __init__(self, alg=None, fld=None, op=None, val=None):
        """
        """
        self.fltr = [{"ALG": alg, "FIELD": fld, "OP": op, "VALUE": val}]

    def __and__(self, other):
        self.fltr = [self.fltr, "AND", other.fltr]
        return self
    
    def __or__(self, other):
        self.fltr = [self.fltr, "OR", other.fltr]
        return self   
    
    def append(self, fltr, bool_op):
        if len(self.fltr) == 1:
            self.fltr = [self.fltr]
        self.fltr.extend([bool_op, fltr])
        return self

class IPDataClient:
    """
    The IpdataAPI class providing blackbox use of the IPCloud Data API.
    This is the main class of the API module. This should be the only class used in
    applictions built around the API.
    """
    BOOLEAN_EXPRESSIONS = ["AND", "OR"]
    IP_TYPE = ['caselaw', 'patents', 'trademarks', 'all']
    ALGORITHMS = ['SQL']
    SPECIAL_CHARS = ["'", "\""]
    OPERATORS = ['EQ', 'IN', 'GT', 'GE', 'LT', 'LE', 'NE', 'IS', 'IS NULL', 'IS NOT NULL', 'STARTSWITH', 'ENDSWITH', 'LIKE', 'CONTAINS']
    AGGREGATIONS = ['COUNT','SUM','MIN','MAX','AVG']

    # class methods
    @classmethod
    def get_ip_types(cls):
        return cls.IP_TYPE

    @classmethod
    def get_alg(cls):
        return cls.ALGORITHMS

    @classmethod
    def get_sc(cls):
        return cls.SPECIAL_CHARS

    @classmethod
    def get_op(cls):
        return cls.OPERATORS
    
    @classmethod
    def get_agg(cls):
        return cls.AGGREGATIONS   

    @classmethod
    def get_bool(cls):
        return cls.BOOLEAN_EXPRESSIONS   

    def __init__(self, api_key):
        """
        IpdataAPI constructor. define the requested API url and
        the user api key required to access the API.
        @param self - the object pointer
        @param api_key - user api key obtianed by registering ipdata api on Clarivate Dev Portal
        @param header - headers required for calling ipdata api
        @param fltr - filter section in api request
        @param fields - fields section in api request
        @param agg - aggregation function section in api request
        @param groupby - groupby section in api request
        @param orderby - orderby section in api request
        @param offset - offset section in api request
        @param limit - limit section in api request
        """
        self.api_key = api_key
        self.base_url = 'https://api.clarivate.com'
        # self.base_url = 'https://api.dev-stable.clarivate.com'
        # self.base_url = 'https://api.test-perf.clarivate.com'
        self.header = None
        self.fltr = None
        self.fields = None
        self.agg = None
        self.groupby = None
        self.orderby = None
        self.offset = None
        self.limit = None
        self.query = None

    def __create_header(self):
        """
        A private method to create the request auth header. 
        """
        if self.header == None:
            self.header = {
                        "X-ApiKey": self.api_key,
                        "Content-Type": "application/json"
                        }

    def __submit_get(self, url):
        """
        A private method to submit a get request to the IPdata server
        @param self - the object pointer
        @param url - API URL to access
        """
        self.__create_header()
        try:
            resp = requests.get(url, headers=self.header)
            resp.raise_for_status()
        except requests.HTTPError as e:
            if resp.status_code in [401, 403]:
                raise AuthError(json.loads(resp.content))
            if resp.status_code == 400:
                raise UserError("Invalid request. Please check your request and try again")
            raise SysError()
        except Exception as e:
            raise SysError()  

        return resp.json()

    def __submit_post(self, url, data):
        """
        A private method to submit a post request to the IPdata server
        @param self - the object pointer
        @param url - API URL to access
        @param data - payload for the HTTP request
        """
        self.__create_header()
        try:
            resp = requests.post(url, data=json.dumps(data), headers=self.header)
            resp.raise_for_status()
        except requests.HTTPError as e:
            if resp.status_code in [401, 403]:
                raise AuthError(json.loads(resp.content))
            if resp.status_code == 400:
                raise UserError("Invalid request. Please check your request and try again")
            raise SysError()
        except Exception as e:
            raise SysError()

        return resp.json()

    def __validate_fltr(self, bool_op=None, alg=None, fld=None, op=None, val=None):
        if bool_op and bool_op not in self.get_bool():
            raise UserError("'bool_op' input is invalid, valid inputs are [{}]".format(','.join(self.get_bool())))
        if not alg or not fld or not op or not val:
            raise UserError("'alg', 'fld', 'op' and 'val' are mandantory aguments")
        if fld not in AVAILABLE_FIELDS:
            raise UserError("'{}' is not an available field, please check and try again".format(fld))
        if alg not in self.get_alg():
            raise UserError("'alg' input is invalid, valid inputs are [{}]".format(','.join(self.get_alg())))
        if op not in self.get_op():
            raise UserError("'op' input is invalid, valid inputs are [{}]".format(','.join(self.get_op())))   

    def build_fltr(self,  fld, op, val, alg="SQL"):
        """
        method to create a filter class obj to construct 'filter' section in api request. 
        """
        self.__validate_fltr(alg=alg, fld=fld, op=op, val=val)
        for char in val:
            if char in self.get_sc():
                val = val.replace(char, "\\" + char)
        return Filter(alg, fld, op, val)

    def build_fltr_combine(self,  fltr_one, fltr_two, bool_op, flat=True):
        """
        method to perfrom bool operation on two filter objs to construct 'filter' section in api request. 
        """
        if not fltr_one or not fltr_two or not bool_op:
            raise UserError("'fltr_one', 'fltr_two' and 'bool_op' are mandantory aguments")
        if not isinstance(fltr_one, Filter) or not isinstance(fltr_two, Filter):
            raise UserError("'fltr_one' and 'fltr_two' need to be 'Filter' objects, please create them using build_fltr()")
        if bool_op not in self.get_bool():
            raise UserError("'bool_op' input is invalid, valid inputs are [{}]".format(','.join(self.get_bool())))
        if bool_op == "AND":
            if flat:
                return fltr_one.append(fltr_two.fltr, "AND")
            return fltr_one & fltr_two
        elif bool_op == "OR":
            if flat:
                return fltr_one.append(fltr_two.fltr, "OR")
            return fltr_one | fltr_two

    def add_fltr_obj(self, fltr):
        """
        method to add constrcuted bool query filters to 'filter' section in api request. (only use for bool filters query use case)
        """
        if not fltr:
            raise UserError("'fltr' is a mandantory agument")
        if not isinstance(fltr, Filter):
            raise UserError("'fltr' needs to be a 'Filter' object, please create them using build_fltr() and construct the bool filters query using build_fltr_combine() and build_fltr_append()")
        if self.fltr:
            raise UserError("'fltr' has already set, use reset_fltr() to reset and try again")
        self.fltr = fltr.fltr

    def add_fltr(self,  fld, op, val, alg="SQL", bool_op=None):
        """
        method to add single filter query to 'filter' section in api request. (only use for single filter query use case)
        """
        self.__validate_fltr(bool_op=bool_op, alg=alg, fld=fld, op=op, val=val)
        if self.fltr:
            raise UserError("'fltr' has already set, use reset_fltr() to reset and try again")
        for char in val:
            if char in self.get_sc():
                val = val.replace(char, "\\" + char)
        self.fltr = {"ALG": alg, "FIELD": fld, "OP": op, "VALUE": val}

    def reset_fltr(self):
        self.fltr = None

    def add_fields_list(self, fields=None):
        """
        method to create 'filed' section in api request, input type restricted to 'list'. 
        """
        if self.fields:
            raise UserError("'fields' has already set, use reset_fields() to reset and try build_fields_list() again")        
        if not fields:
            raise UserError("'fields' is mandantory for build_fields_list()")
        if not isinstance(fields, list):
            raise UserError("build_fields_list() only allow 'list' type 'fields'")
        for fld in fields:
            if fld not in AVAILABLE_FIELDS:
                raise UserError("'{}' is not an available field, please check and try add_fields_list() again".format(fld))
        self.fields = fields    
 
    def add_fields_alias(self, fields=None):
        """
        method to create 'filed' section in api request, input type restricted to 'dict'. 
        """
        if self.fields:
            raise UserError("'fields' has already set, use reset_fields() to reset and try build_fields_alias() again")              
        if not fields:
            raise UserError("'fields' is mandantory for build_fields_alias()")
        if not isinstance(fields, dict):
            raise UserError("build_fields_alias() only allow 'dict' type 'fields'")
        for fld in fields.keys():
            if fld not in AVAILABLE_FIELDS:
                raise UserError("'{}' is not an available field, please check and try add_fields_alias() again".format(fld))
        self.fields = fields

    def reset_fields(self):
        self.fields = None

    def __validate_agg(self, func=None, fld=None, alias=None):
        if not func or not fld or not alias:
            raise UserError("'func', 'fld' and 'alias' are mandantory for build_agg() and build_agg_append()")
        if not isinstance(func, str) or not isinstance(fld, str) or not isinstance(alias, str):
            raise UserError("'func', 'fld' and 'alias' only allow 'str' type for build_agg() and build_agg_append()")
        if func not in self.get_agg():
            raise UserError("'func' input is invalid, valid inputs are [{}]".format(','.join(self.get_agg())))   
        if fld not in AVAILABLE_FIELDS:
            raise UserError("'{}' is not an available field, please check and try add_agg() again".format(fld))
        
    def add_agg(self, func=None, fld=None, alias=None):
        """
        method to create 'agg' section in api request. 
        """        
        self.__validate_agg(func=func, fld=fld, alias=alias)
        if self.agg: # append new agg to existing
            self.agg.append({"FUNC": func, "FIELD": fld, "ALIAS": alias})
        else:
            self.agg = [{"FUNC": func, "FIELD": fld, "ALIAS": alias}]

    def reset_agg(self):
        self.agg = None

    def add_groupby(self, fields=None):
        """
        method to create 'groupby' section in api request. 
        """
        if self.groupby:
            raise UserError("'groupby' has already set, use reset_groupby() to reset and try build_groupby() again")        
        if not fields:
            raise UserError("'fields' is mandantory for build_groupby()")
        if not isinstance(fields, list):
            raise UserError("build_groupby() only allow 'list' type 'fields'")
        for fld in fields:
            if fld not in AVAILABLE_FIELDS:
                raise UserError("'{}' is not an available field, please check and try add_groupby() again".format(fld))
        self.groupby = fields    

    def reset_groupby(self):
        self.groupby = None

    def __validate_orderby(self, fld=None, order=None):
        if not fld or not order:
            raise UserError("'fld' and 'order' are mandantory for build_orderby() and build_orderby_append()")
        if not isinstance(fld, str) or not isinstance(order, (str, bool)):
            raise UserError("'fld' only allow 'str' type and 'order' allow 'str' or 'bool' type for build_orderby() and build_orderby_append()")
        if fld not in AVAILABLE_FIELDS:
            raise UserError("'{}' is not an available field, please check and try add_orderby() again".format(fld))

    def add_orderby(self, fld=None, order=None):
        """
        method to create 'orderby' section in api request. 
        """
        self.__validate_orderby(fld=fld, order=order)
        if self.orderby: # append new orderby field to existing
            self.orderby.append({"{}".format(fld): order})
        else:
            self.orderby = [{"{}".format(fld): order}]

    def reset_orderby(self):
        self.orderby = None

    def add_limit_and_offset(self, limit=10, offset=0):
        """
        method to create 'limit' and 'offset' section in api request. 
        """
        if self.limit is not None:
            raise UserError("'limit' has already set, use reset_limit() to reset and try add_limit_and_offset() again") 
        if limit is None:
            raise UserError("'limit' is mandantory for add_limit()")
        if not isinstance(limit, int):
            raise UserError("'limit' only allow 'int' type for add_limit()")
        if self.offset is not None:
            raise UserError("'offset' has already set, use reset_offset() to reset and try add_limit_and_offset() again")
        if offset is None:
            raise UserError("'offset' is mandantory for add_offset()")
        if not isinstance(offset, int):
            raise UserError("'offset' only allow 'int' type for add_offset()")
        self.limit = limit
        self.offset = offset

    def reset_limit_and_offset(self):
        self.limit = None
        self.offset = None

    def search(self, ip_type="caselaw"):
        """
        A private method to query against all data source
        @param self - the object pointer
        @param payload - payload for the query
        """
        if ip_type in self.get_ip_types():
            url = urljoin(self.base_url, ip_type+"/search")
            print(url)
        else:
            raise UserError("Invalid ip source type. Please check your request and try again")
        if not self.fltr:
            raise UserError("'fltr' is required in request. Please check your request and try again")
        self.query = Query(filter=self.fltr)
        print(json.dumps(self.query.create_query(self.fields, self.agg, self.groupby, self.orderby, self.offset, self.limit), indent=4))
        return self.__submit_post(url, self.query.create_query(self.fields, self.agg, self.groupby, self.orderby, self.offset, self.limit))

    def get_doc(self, id, ip_type="caselaw"):
        if not id:
            raise UserError("'id' for the document is required for document retrieval!")
        if ip_type in self.get_ip_types():
            url = urljoin(self.base_url, ip_type + "/document/json/" + str(id))
            print(url)
        else:
            raise UserError("Invalid ip source type. Please check your request and try again")
        return self.__submit_get(url)