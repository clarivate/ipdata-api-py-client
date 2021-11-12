from .error import AuthError, SysError, UserError

class Query:
    """ 
    The Urls class will handle all of the URLs. this class will store 
    and serve all of the URL strings useful to the IPCloud Data API.
    """
    def __init__(self, filter=None):
        """
        The constructor which defines all of the URLs used by the API.
        When adding new API functionality the URL needs to be added here.
        Examples abound of the format used by this implementation of the API.
        @param self - the object pointer
        @param feature - functionality of the api. possible values are 'records'(under dev), 'search'(available), 'lookup'(under dev)
        """
        self.filter = None 
        self.fields = None
        self.agg = None
        self.groupby = None
        self.orderby = None
        self.offset = None
        self.limit = None
        self.query = None
        self.build_basic_query(filter)

    ### Helper functions to build query ###
    def build_basic_query(self, filter):
        if filter is None:
            raise UserError("'filter' is required in request. Please check your request and try again")
        self.filter = filter
        self.query = {"QUERY": self.filter}

    def add_fields(self, fields):
        # fields can be a flat list or dictionary (for aliased fields)
        self.fields = fields
        self.query.update({"FIELDS": self.fields})

    def add_agg(self, agg):
        # can support a list of aggregations, so this function is written to be able to append multiple
        self.agg = agg
        self.query.update({"AGG": self.agg})

    def add_groupby(self, groupby):
        self.groupby = groupby
        self.query.update({"GROUPBY": self.groupby})

    def add_orderby(self, orderby):
        self.orderby = orderby
        self.query.update({"ORDERBY": self.orderby})

    def add_limit(self, limit):
        self.limit = limit
        self.query.update({"LIMIT": self.limit})

    def add_offset(self, offset):
        self.offset = offset
        self.query.update({"OFFSET": self.offset})

    def create_query(self, fields, agg, groupby, orderby, offset, limit):
        if fields is not None:
            self.add_fields(fields)
        if agg is not None:
            self.add_agg(agg)
        if groupby is not None:
            self.add_groupby(groupby)
        if orderby is not None:
            self.add_orderby(orderby)
        if limit is not None:
            self.add_limit(limit)
        if offset is not None:
            self.add_offset(offset)
        return self.query