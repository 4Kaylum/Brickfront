from xml.etree import ElementTree as ET
from requests import get
from .errors import InvalidRequest, InvalidApiKey, InvalidLoginCredentials, InvalidSetID
from .build import Build
from .review import Review


class Client(object):
    '''
    A frontend authenticator for Brickset.com's API.
    All endpoints require an API key.

    :param str apiKey: The API key you got from Brickset.
    :param bool raiseError: (optional) Whether or not you want an error to be raised on an invalid API key.
    :raises brickfront.errors.InvalidApiKey: If the key provided is invalid.
    '''

    ENDPOINT = 'http://brickset.com/api/v2.asmx/{}'

    def __init__(self, apiKey, raiseError=True):
        self.apiKey = apiKey
        self.userHash = ''  # Would be None but is used elsewhere, so has to be a blank string

        # Check the provided key
        if not self.checkKey() and raiseError:
            raise InvalidApiKey('The provided API key `{}` was invalid.'.format(apiKey))


    @staticmethod
    def checkResponse(request):
        '''
        Returns if a request has an okay error code, otherwise raises InvalidRequest.
        '''

        # Check the status code of the returned request
        if str(request.status_code)[0] not in ['2', '3']:
            w = str(request.text).split('\\r')[0][2:]
            raise InvalidRequest(w)
        return


    def checkKey(self, key=None):
        '''
        Checks that an API key is valid.

        :param str key: (optional) A key that you want to check the validity of. Defaults to the one provided on initialization.
        :returns: If the key is valid, this method will return ``True``.
        :rtype: `bool`
        :raises: :class:`brickfront.errors.InvalidApiKey`
        '''

        # Get site
        url = Client.ENDPOINT.format('checkKey')
        if not key: key = self.apiKey
        params = {
            'apiKey': key or self.apiKey
        }
        returned = get(url, params=params)
        self.checkResponse(returned)

        # Parse and return
        root = ET.fromstring(returned.text)
        if root.text == 'OK':
            return True
        raise InvalidApiKey('The provided API key `{}` was invalid.'.format(key))


    def login(self, username, password):
        '''
        Logs into Brickset as a user, returning a userhash, which can be used in other methods.
        The user hash is stored inside the client (:attr:`userHash`).

        :param str username: Your Brickset username.
        :param str password: Your Brickset password.
        :returns: If the login is valid, this will return ``True``.
        :rtype: `bool`
        :raises: :class:`brickfront.errors.InvalidLoginCredentials`
        '''

        # Get the site
        url = Client.ENDPOINT.format('login')
        params = {
            'apiKey': self.apiKey,
            'username': username,
            'password': password,
        }
        returned = get(url, params=params)
        self.checkResponse(returned)
        root = ET.fromstring(returned.text)

        # Determine whether they logged in correctly
        if root.text.startswith('ERROR'):
            self.userHash = ''
            raise InvalidLoginCredentials('The provided username and password were unable to authenticate.')
        self.userHash = root.text
        return True


    def getSets(self, **kwargs):
        '''
        A way to get different sets from a query.
        All parameters are optional, but you should probably use some (so that you get results)

        :param str query: The thing you're searching for.
        :param str theme: The theme of the set.
        :param str subtheme: The subtheme of the set.
        :param str setNumber: The LEGO set number.
        :param str year: The year in which the set came out.
        :param int owned: Whether or not you own the set. Only works when logged in with :meth:`login`. Set to `1` to make true.
        :param int wanted: Whether or not you want the set. Only works when logged in with :meth:`login`. Set to `1` to make true.
        :param str orderBy: How you want the set ordered. Accepts 'Number', 'YearFrom', 'Pieces', 'Minifigs', 'Rating', 'UKRetailPrice', 'USRetailPrice', 'CARetailPrice', 'EURetailPrice', 'Theme', 'Subtheme', 'Name', 'Random'. Add 'DESC' to the end to sort descending, e.g. NameDESC. Case insensitive. Defaults to 'Number'.
        :param int pageSize: How many results are on a page. Defaults to 20.
        :param int pageNumber: The number of the page you're looking at. Defaults to 1.
        :param str userName: The name of a user whose sets you want to search.
        :returns: A list of :class:`brickfront.build.Build` objects.
        :rtype: list
        '''

        # Generate a dictionary to send as parameters
        params = {
            'apiKey':     self.apiKey,
            'userHash':   self.userHash,
            'query':      kwargs.get('query', ''),
            'theme':      kwargs.get('theme', ''),
            'subtheme':   kwargs.get('subtheme', ''),
            'setNumber':  kwargs.get('setNumber', ''),
            'year':       kwargs.get('year', ''),
            'owned':      kwargs.get('owned', ''),
            'wanted':     kwargs.get('wanted', ''),
            'orderBy':    kwargs.get('orderBy', 'Number'),
            'pageSize':   kwargs.get('pageSize', '20'),
            'pageNumber': kwargs.get('pageNumber', '1'),
            'userName':   kwargs.get('userName', '')
        }
        url = Client.ENDPOINT.format('getSets')
        returned = get(url, params=params)
        self.checkResponse(returned)

        # Construct the build objects and return them graciously
        root = ET.fromstring(returned.text)
        return [Build(i, self) for i in root]


    def getSet(self, setID):
        '''
        Gets the information of one specific build using its Brickset set ID.

        :param str setID: The ID of the build from Brickset.
        :returns: A single Build object.
        :rtype: :class:`brickfront.build.Build`
        :raises brickfront.errors.InvalidSetID: If no sets exist by that ID.
        '''

        params = {
            'apiKey': self.apiKey,
            'userHash': self.userHash,
            'setID': setID
        }
        url = Client.ENDPOINT.format('getSet')
        returned = get(url, params=params)
        self.checkResponse(returned)

        # Put it into a Build class
        root = ET.fromstring(returned.text)
        v = [Build(i, self) for i in root]

        # Return to user
        try:
            return v[0]
        except IndexError:
            raise InvalidSetID('There is no set with the ID of `{}`.'.format(setID))


    def getRecentlyUpdatedSets(self, minutesAgo):
        '''
        Gets the information of recently updated sets.

        :param int minutesAgo: The amount of time ago that the set was updated.
        :returns: A list of Build instances that were updated within the given time.
        :rtype: list
        .. warning:: An empty list will be returned if there are no sets in the given time limit.
        '''

        params = {
            'apiKey': self.apiKey,
            'minutesAgo': minutesAgo
        }
        url = Client.ENDPOINT.format('getRecentlyUpdatedSets')
        returned = get(url, params=params)
        self.checkResponse(returned)

        # Parse them in to build objects
        root = ET.fromstring(returned.text)
        return [Build(i, self) for i in root]


    def getAdditionalImages(self, setID):
        '''
        Gets a list of URLs containing images of the set.

        :param str setID: The ID of the set you want to grab the images for.
        :returns: A list of URL strings.
        :rtype: list
        .. warning:: An empty list will be returned if there are no additional images, or if the set ID is invalid.
        '''

        params = {
            'apiKey': self.apiKey,
            'setID': setID
        }
        url = Client.ENDPOINT.format('getAdditionalImages')
        returned = get(url, params=params)
        self.checkResponse(returned)

        # I really fuckin hate XML
        root = ET.fromstring(returned.text)
        urlList = []

        for imageHolder in root:
            urlList.append(imageHolder[-1].text)
        return urlList


    def getReviews(self, setID):
        '''
        Get the reviews for a set.

        :param str setID: The ID of the set you want to get the reviews of.
        :returns: A list of reviews.
        :rtype: List[:class:`brickfront.review.Review`]
        .. warning:: An empty list will be returned if there are no reviews, or if the set ID is invalid.
        '''

        params = {
            'apiKey': self.apiKey,
            'setID': setID
        }
        url = Client.ENDPOINT.format('getReviews')
        returned = get(url, params=params)
        self.checkResponse(returned)

        # Parse into review objects
        root = ET.fromstring(returned.text)
        return [Review(i) for i in root]


    def getInstructions(self, setID):
        '''
        Get the instructions for a set.

        :param str setID: The ID for the set you want to get the instructions of.
        :returns: A list of URLs to instructions.
        :rtype: List[`dict`]
        .. warning:: An empty list will be returned if there are no instructions, or if the set ID is invalid.
        '''

        params = {
            'apiKey': self.apiKey,
            'setID': setID
        }
        url = Client.ENDPOINT.format('getInstructions')
        returned = get(url, params=params)
        self.checkResponse(returned)

        # Parse into review objects
        root = ET.fromstring(returned.text)
        return [i[0].text for i in [o for o in root]]
