from requests import get as _get
from xml.etree import ElementTree as _ET
from .errors import InvalidOrderType as _InvalidOrderType
from .errors import InvalidRequest as _InvalidRequest
from .build import Build as _Build


class Client(object):
    '''
    A frontend authenticator for Brickset.com's API.
    All endpoints require an API key.

    :param str apiKey: The API key you got from Brickset.
    '''

    _base = 'http://brickset.com/api/v2.asmx/{}?'

    def __init__(self, apiKey: str):

        self._apiKey = apiKey
        self._getURL = lambda x, y: Client._base.format(x) + '&'.join(y)

    def getSets(self, *, query: str='', theme: str='', subtheme: str='', setNumber: str='', year: int='', orderBy: str='Number', pageSize: int=20):
        '''
        A way to get different sets from a query.
        All parameters are optional, but you should *probably* use some.

        :param str query: The search term for which you're looking.
        :param str theme: The theme of the set you're looking for.
        :param str subtheme: The subtheme that you're looking for.
        :param str setNumber: The set number of the set.
        :param int year: The year in which the set came out.
        :param str orderBy: How you want to order the results. Valid options are `Number`, `YearFrom`, `Pieces`, `Minifigs`, `Rating`, `UKRetailPrice`, `USRetailPrice`, `CARetailPrice`, `EURetailPrice`, `Theme`, `Subtheme`, `Name`, `Random`. Add 'DESC' to the end to sort descending, e.g. `NameDESC`. Defaults to `Number`. Values are case sensitive.
        :param int pageSize: How many sets should be returned. Defaults to 20.
        :returns: A list of LEGO sets.
        :rtype: List[:class:`brickfront.build.Build`]
        '''

        # Make sure that orderBy is valid
        if orderBy not in ['Number', 'YearFrom', 'Pieces', 'Minifigs', 'Rating', 
                'UKRetailPrice', 'USRetailPrice', 
                'CARetailPrice', 'EURetailPrice', 'Theme']:
            raise _InvalidOrderType('You have not specified a valid ordering type.')


        # Generate a dictionary to post
        values = {
                'apiKey': self._apiKey,
                'query': query,
                'theme': theme,
                'subtheme': subtheme,
                'setNumber': setNumber,
                'year': year,
                'orderBy': orderBy,
                'pageSize': pageSize,
                'userHash': '',
                'owned': '',
                'wanted': '',
                'userName': '',
                'pageNumber': 1
            }

        # Format into a link
        sendValues = []
        for i, o in values.items():
            addedValue = '{}={}'.format(i, o)
            sendValues.append(addedValue)

        # Send the GET request.
        returned = _get(self._getURL('getSets', sendValues))
        
        # Make sure all is well
        if returned.status_code is not 200:
            w = str(returned.text).split('\\r')[0][2:]
            raise _InvalidRequest(w)

        root = _ET.fromstring(returned.text)
        return [_Build(i) for i in root]

