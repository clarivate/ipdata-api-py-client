"""
Expected errors in the ip module
"""

class Error(Exception):
    ''' Stub error class to be used by other exceptions '''
    def __init__(self, desc):
        super().__init__()
        self.desc = desc

    def __str__(self):
        return "Error: {}".format(self.desc)

class AuthError(Error):
    ''' Error class to handle user auth issues '''

class SysError(Error):
    ''' Error class to handle unhandled system errors '''
    def __init__(self):
        super().__init__("Something went wrong, please contact support")

class UserError(Error):
    ''' Error class to handle user errors '''
