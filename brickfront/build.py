class Build(object):
    '''
    A class holding the information of a LEGO set. Some attributes may be ``None``. 
    There is no need to create an instance of a ``Build`` object yourself - it won't go well.

    :ivar str setID: The ID of the set from Brickset.
    :ivar str number: The number of the set on Brickset.
    :ivar int variant: The variant of the LEGO set.
    :ivar str year: The `year in which the set came out.
    :ivar str theme: The theme of the set.
    :ivar str themeGroup: The type of the theme.
    :ivar str subtheme: Any other theme that the set may belong to.
    :ivar int pieces: The number of pieces in the set.
    :ivar int minifigs: The number of minifigs that the set may come with.
    :ivar str imageURL: The URL of the image of the set.
    :ivar str bricksetURL: The link to the Brickset page of the set.
    :ivar bool released: Whether or not the set has been released.
    :ivar str priceUK: The UK price of the set.
    :ivar str priceUS: The US price of the set.
    :ivar str priceCA: The CA price of the set.
    :ivar str priceEU: The EU price of the set.
    :ivar float rating: The Brickset rating of the LEGO set.
    :ivar list additionalImages: A list of image URLs.
    :ivar list reviews: A list of :class:`brickfront.review.Review` objects representing reviews.
    :ivar list instructions: List[`str`]
    '''

    def __init__(self, data, userHash, client):

        self.raw = data
        self._client = client

        if userHash != '':
            del data[20]

        self.setID = self.id = str(data[0].text)
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

        # A simple cache of these items - defaulting to nonexistent
        self._additionalImages = None 
        self._reviews = None
        self._instructions = None


    def getAdditionalImages(self):
        '''
        The same as calling `client.getAdditionalImages(build.setID)`

        :returns: A list of URL strings.
        :rtype: List[`str`]
        '''

        self._additionalImages = self._client.getAdditionalImages(self.setID)
        return self._additionalImages


    @property 
    def additionalImages(self):
        if self._additionalImages is None:
            self._additionalImages = self.getAdditionalImages()
        return self._additionalImages


    def getReviews(self):
        '''
        The same as calling `client.getReviews(build.setID)`

        :returns: A list of reviews.
        :rtype: List[:class:`brickfront.review.Review`]
        '''

        self._reviews = self._client.getReviews(self.setID)
        return self._reviews


    @property
    def reviews(self):
        if self._reviews is None:
            self._reviews = self.getReviews()
        return self._reviews


    def getInstructions(self):
        '''
        The same as calling `client.getInstructions(build.setID)`

        :returns: A list of instructions.
        :rtype: List[`str`]
        '''

        self._instructions = self._client.getInstructions(self.setID)
        return self._instructions


    @property 
    def instructions(self):
        if self._instructions is None:
            self._instructions = self.getInstructions()
        return self._instructions
