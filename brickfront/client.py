from requests import get as _get
from xml.etree import ElementTree as _ET
from .errors import InvalidRequest as _InvalidRequest
from .errors import InvalidKey as _InvalidKey
from .errors import InvalidLogin as _InvalidLogin
from .errors import InvalidSetID as _InvalidSetID
from .build import Build as _Build
from .review import Review as _Review


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
        Returns a HTTP request.
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
        Returns if a request has an okay error code, otherwise raises InvalidRequest.
        '''

        # Check the status code of the returned request
        if str(request.status_code)[0] not in ['2', '3']:
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

    def getSet(self, setID: str) -> _Build:
        '''
        Gets the information of one build, using its Brickset set ID.

        :param str setID: The ID of the build from Brickset.
        :returns: A single LEGO set object.
        :rtype: :class:`brickfront.build.Build`
        :raises brickfront.errors.InvalidSetID: If no sets exist by that ID.
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
        v = [_Build(i, self._userHash) for i in root]
        if len(v) == 0:
            raise _InvalidSetID
        return v[0]

    def getRecentlyUpdatedSets(self, minutesAgo: int) -> list:
        '''
        Gets the information of recently updated sets.

        :param int minutesAgo: The amount of time ago that the set was updated.
        :returns: A list of sets that were updated within the given time.
        :rtype: List[:class:`brickfront.build.Build`]
        '''

        values = {
            'apiKey': self._apiKey,
            'minutesAgo': minutesAgo
        }

        # Send the GET request
        returned = _get(self._getURL('getRecentlyUpdatedSets', values))

        # Make sure all is well
        self._isOkayRequest(returned)

        root = _ET.fromstring(returned.text)
        return [_Build(i, self._userHash) for i in root]

    def getAdditionalImages(self, setID: str) -> list:
        '''
        Gets a list of URLs containing images of the set.

        :param str setID: The ID of the set you want to grab the images for.
        :returns: A list of URL strings.
        :rtype: List[`str`]
        .. warning:: If a set ID is invalid, an empty list will be returned.
        '''

        values = {
            'apiKey': self._apiKey,
            'setID': setID
        }

        # Send the GET request
        returned = _get(self._getURL('getAdditionalImages', values))

        # Make sure all is well
        self._isOkayRequest(returned)

        root = _ET.fromstring(returned.text)
        urlList = []

        for imageHolder in root:
            urlList.append(imageHolder[-1].text)

        return urlList

    def getReviews(self, setID: str) -> list:
        '''
        Get the reviews for a set.

        :param str setID: The ID of the set you want to get the reviews of.
        :returns: A list of reviews.
        :rtype: List[:class:`brickfront.review.Review`]
        .. warning:: If a set ID is invalid, an empty list will be returned.
        '''

        values = {
            'apiKey': self._apiKey,
            'setID': setID
        }

        # Send the GET request
        returned = _get(self._getURL('getReviews', values))

        # Make sure all is well
        self._isOkayRequest(returned)

        root = _ET.fromstring(returned.text)
        return [_Review(i) for i in root]
