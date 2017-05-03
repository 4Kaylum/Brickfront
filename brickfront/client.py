from requests import get as _get
from xml.etree import ElementTree as _ET
from .errors import InvalidRequest as _InvalidRequest
from .errors import InvalidKey as _InvalidKey
from .errors import InvalidLogin as _InvalidLogin
from .build import Build as _Build


class Client(object):
    '''
    A frontend authenticator for Brickset.com's API.
    All endpoints require an API key.

    :param str apiKey: The API key you got from Brickset.
    :raises brickfront.errors.InvalidKey: If the key provided is invalid.
    '''

    _base = 'http://brickset.com/api/v2.asmx/{}?'

    def __init__(self, apiKey: str):

        self._apiKey = apiKey
        self._userHash = ''

        if not self.checkKey():
            raise _InvalidKey('The provided key was invalid.')

    def _getURL(self, method: str, arguments) -> str:
        '''
        Returns a HTTP request
        '''

        # Format the base
        x = Client._base.format(method)

        # Format the url with the arguments
        if type(arguments) == str:
            x = x + arguments
        elif type(arguments) == list:
            x = x + '&'.join(arguments)
        elif type(arguments) == dict:
            sendValues = []
            for i, o in arguments.items():
                addedValue = '{}={}'.format(i, o)
                sendValues.append(addedValue)
            x = x + '&'.join(sendValues)
        else:
            raise ValueError('Passed invalid type.')

        # Return the valid call url
        return x

    def _isOkayRequest(self, request) -> bool:
        '''
        Returns if a request has an okay error code, otherwise raises
        InvalidRequest
        '''

        # Check the status code of the returned request
        if request.status_code is not 200:
            w = str(request.text).split('\\r')[0][2:]
            raise _InvalidRequest(w)
        return

    def checkKey(self) -> bool:
        '''
        Checks that an API key is valid.

        :returns: Whether the key is valid or not.
        :rtype: `bool`
        '''

        # Get site
        returned = _get(self._getURL('checkKey', 'apiKey={}'.format(self._apiKey)))
        
        # Make sure all is well
        self._isOkayRequest(returned)

        # Parse XML
        root = _ET.fromstring(returned.text)
        
        # Return bool
        return root.text == 'OK'

    def login(self, username: str, password: str) -> bool:
        '''
        Logs into Brickset as a user, returning a userhash, which can be used in other methods.
        The userhash is stored inside the client.

        :param str username: Your Brickset username.
        :param str password: Your Brickset password.
        :returns: A boolean value of whether or not the login request was done properly.
        :rtype: `bool`
        :raises brickfront.errors.InvalidLogin: If your login details are incorrect.
        '''

        # These are the values of the arguments that are to be sent to the site
        values = {
            'apiKey': self._apiKey,
            'username': username,
            'password': password
        }

        # Get a login
        returned = _get(self._getURL('login', values))

        # Make sure that you didn't send anything to the wrong URL
        self._isOkayRequest(returned)

        # Check if the login is invalid
        root = _ET.fromstring(returned.text)
        if root.text.startswith('ERROR'):
            raise _InvalidLogin(root.text[7:])

        # Store the user hash
        self._userHash = root.text
        return True

    def getSets(self, **kwargs) -> list:
        '''
        A way to get different sets from a query.
        All parameters are optional, but you should *probably* use some.

        :param str query: The thing you're searching for.
        :param str theme: The theme of the set.
        :param str subtheme: The subtheme of the set.
        :param str setNumber: The LEGO set number.
        :param str year: The year in which the set came out.
        :param str owned: Whether or not you own the set. Only works when logged in with :meth:`login`. Set to `1` to make true.
        :param str wanted: Whether or not you want the set. Only works when logged in with :meth:`login`. Set to `1` to make true.
        :param str orderBy: How you want the set ordered. Accepts 'Number', 'YearFrom', 'Pieces', 'Minifigs', 'Rating', 'UKRetailPrice', 'USRetailPrice', 'CARetailPrice', 'EURetailPrice', 'Theme', 'Subtheme', 'Name', 'Random'. Add 'DESC' to the end to sort descending, e.g. NameDESC. Case insensitive. Defaults to 'Number'.
        :param str pageSize: How many results are on a page. Defaults to 20.
        :param str pageNumber: The number of the page you're looking at. Defaults to 1.
        :param str userName: The name of a user whose sets you want to search.
        :returns: A list of LEGO sets.
        :rtype: List[:class:`brickfront.build.Build`]
        '''

        # Generate a dictionary to post
        values = {
            'apiKey': self._apiKey,
            'userHash': self._userHash,
            'query': kwargs.get('query', ''),
            'theme': kwargs.get('theme', ''),
            'subtheme': kwargs.get('subtheme', ''),
            'setNumber': kwargs.get('setNumber', ''),
            'year': kwargs.get('year', ''),
            'owned': kwargs.get('owned', ''),
            'wanted': kwargs.get('wanted', ''),
            'orderBy': kwargs.get('orderBy', 'Number'),
            'pageSize': kwargs.get('pageSize', '20'),
            'pageNumber': kwargs.get('pageNumber', '1'),
            'userName': kwargs.get('userName', '')
        }

        # Send the GET request.
        returned = _get(self._getURL('getSets', values))
        
        # Make sure all is well
        self._isOkayRequest(returned)

        root = _ET.fromstring(returned.text)
        return [_Build(i, self._userHash) for i in root]

    def getSet(self, setID: str) -> list:
        '''
        Gets the information of one build, using its Brickset set ID

        :param str setID: The ID of the build from Brickset.
        :returns: A single LEGO set in a list. Will return an empty list if no sets are found.
        :rtype: List[:class:`brickfront.build.Build`]
        :raises brickfront.errors.InvalidRequest: If the site doesn't like the sent request.
        '''

        values = {
            'apiKey': self._apiKey,
            'userHash': self._userHash,
            'setID': setID
        }

        # Send the GET request.
        returned = _get(self._getURL('getSet', values))
        
        # Make sure all is well
        self._isOkayRequest(returned)

        root = _ET.fromstring(returned.text)
        return [_Build(i, self._userHash) for i in root]
