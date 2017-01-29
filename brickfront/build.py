class Build(object):
    '''
    A class holding the information of a LEGO set. Some attributes may be `None`. Check them before using them.

    Called automatically by other functions. Do not manually call.

    :ivar setID: The `int` ID of the set on Brickset.
    :ivar number: The number of the set on Brickset, held as a `str`.
    :ivar variant: The `int` variant of the LEGO set.
    :ivar year: The `str` year in which the set came out.
    :ivar theme: `str` The theme of the set.
    :ivar themeGroup: `str` The type of the theme.
    :ivar subtheme: `str` Any other theme that the set may belong to.
    :ivar pieces: `int` The number of pieces in the set.
    :ivar minifigs: `int` The number of minifigs that the set may come with.
    :ivar imageURL: `str` The URL of the image of the set.
    :ivar bricksetURL: `str` The link to the Brickset page of the set.
    :ivar released: `bool` Whether or not the set has been released.
    :ivar priceUK: `str` The UK price of the set.
    :ivar priceUS: `str` The US price of the set.
    :ivar priceCA: `str` The CA price of the set.
    :ivar priceEU: `str` The EU price of the set.
    :ivar rating: `float` The Brickset rating of the LEGO set.
    '''

    def __init__(self, data, userHash=''):

        self.raw = data

        if userHash != '':
            del data[20]

        self.setID = int(data[0].text)
        self.number = data[1].text
        self.variant = int(data[2].text)
        self.name = data[3].text
        self.year = data[4].text
        self.theme = data[5].text
        self.themeGroup = data[6].text
        self.subtheme = data[7].text
        try: z = int(data[8].text)
        except TypeError: z = None
        self.pieces = z
        try: z = int(data[9].text)
        except TypeError: z = None
        self.minifigs = z
        self.imageURL = data[14].text
        self.bricksetURL = data[15].text
        self.priceUK = data[23].text
        self.priceUS = data[24].text
        self.priceCA = data[25].text
        self.priceEU = data[26].text
        try: z = float(data[29].text)
        except TypeError: z = None
        self.rating = z
        try:
            z = {
                'true': True,
                '0': False,
                '1': True,
                'false': False,
                'none': False
            }[str(data[16].text).lower()]
        except KeyError:
            z = data[16].text 
        self.released = z
