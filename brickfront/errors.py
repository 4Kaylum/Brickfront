class InvalidRequest(Exception):
    '''
    The request that was sent to the server was invalid.
    '''

    pass


class InvalidKey(Exception):
    '''
    The API key provided was invalid and cannot be used.
    '''

    pass


class InvalidLogin(Exception):
    '''
    The login credentials used were invalid.
    '''

    pass
