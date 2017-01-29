class Build(object):
    '''
    A class holding the information of a LEGO set. Some attributes may be `None`. Check them before using them.
    
    Called automatically by other functions. Do not manually call.

    :ivar setID: The ID of the set on Brickset.
    :ivar number: The number of the set on Brickset.
    :ivar variant: The variant of the LEGO set.
    :ivar year: The year in which the set came out.
    :ivar theme: The theme of the set.
    :ivar themeGroup: The type of the theme.
    :ivar subtheme: Any other theme that the set may belong to.
    :ivar pieces: The number of pieces in the set.
    :ivar minifigs: The number of minifigs that the set may come with.
    :ivar imageURL: The URL of the image of the set.
    :ivar bricksetURL: The link to the Brickset page of the set.
    :ivar released: Whether or not the set has been released.
    :ivar priceUK: The UK price of the set.
    :ivar priceUS: The US price of the set.
    :ivar priceCA: The CA price of the set.
    :ivar priceEU: The EU price of the set.
    :ivar rating: The Brickset rating of the LEGO set.
    '''

    def __init__(self, data):

        self.raw = data

        self.setID = data[0].text 
        self.number = data[1].text 
        self.variant = data[2].text 
        self.name = data[3].text 
        self.year = data[4].text 
        self.theme = data[5].text
        self.themeGroup = data[6].text
        self.subtheme = data[7].text 
        self.pieces = data[8].text 
        self.minifigs = data[9].text
        self.imageURL = data[14].text
        self.bricksetURL = data[15].text
        self.released = {'true':True,'0':False}[data[16].text]
        self.priceUK = data[23].text
        self.priceUS = data[24].text
        self.priceCA = data[25].text
        self.priceEU = data[26].text
        self.rating = data[29].text
