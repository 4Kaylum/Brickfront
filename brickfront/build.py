from datetime import datetime


class Build(object):
    '''
    A class holding the information of a LEGO set. Some attributes may be ``None``. 
    There is no need to create an instance of a ``Build`` object yourself - it won't go well.

    :ivar int setID: The set ID, as used on Brickset.
    :ivar str number: The LEGO ID number of the set.
    :ivar int variant: The variant of the set, as used on Brickset.
    :ivar str name: The name of the set.
    :ivar str year: The year the set was released.
    :ivar str theme: The theme of the set.
    :ivar str themeGroup: The theme group, as used on /browse/sets
    :ivar str subtheme: The subtheme of the set.
    :ivar int pieces: How many pieces the set has.
    :ivar int minifigs: The amount of minifigs what come with the set.
    :ivar str imageURL: A URL to an image of the set.
    :ivar str bricksetURL: The URL to the page for the set on Brickset.
    :ivar bool released: Whether or not the set is released.
    :ivar bool owned: Whether or not own the set. Only works when logged in.
    :ivar bool wanted: Whether or not you want the set. Only works when logged in.
    :ivar int quantityOwned: The number of these that you own. Only works when logged in.
    :ivar int ACMDataCount: Number of ACM records you have modified for this set.
    :ivar str userNotes: The notes that you have on the product. Only works when logged in.
    :ivar int ownedByTotal: The number of people who own this set.
    :ivar int wantedByTotal: The number of people who want this set.
    :ivar str priceUK: The price of the set.
    :ivar str priceUS: The price of the set.
    :ivar str priceCA: The price of the set.
    :ivar str priceEU: The price of the set.
    :ivar datetime.datetime dateAddedToStore: The date that the set was added to the US LEGO store website.
    :ivar datetime.datetime dateRemovedFromStore: The date that the set was removed from the US LEGO store website. If ``None``, then the set is still available.
    :ivar float rating: The overall rating of the set on Brickset.
    :ivar int reviewCount: How many reviews the set has on Brickset.
    :ivar str packagingType: How the set is packaged
    :ivar str availability: Where the set is available.
    :ivar int instructionsCount: How many sets of instructions the set has.
    :ivar int additionalImageCount: How many additional images the set has.
    :ivar str EAN: The standard barcode number of the set.
    :ivar str UPC: The standard barcode number of the set.
    :ivar str description: The description of the set.
    :ivar datetime.datetime lastUpdated: When the set was last updated on Brickset.
    :ivar list additionalImages: The URLs to the additional images of the set.
    :ivar list reviews: A list of :class:`brickfront.review.Review` objects for the reviews of the set.
    '''

    def __init__(self, data, client):

        self.raw = data
        self._client = client

        # Set up the attributes of this class
        applicableTags = [
            'setID',
            'number',
            ['numberVariant', 'variant'],
            'name',
            'year',
            'theme',
            'themeGroup',
            'subtheme',
            'pieces',
            'minifigs',
            'imageURL',
            'bricksetURL',
            'released',
            'owned',
            'wanted',
            ['qtyOwned', 'quantityOwned'],
            'ACMDataCount',
            'userNotes',
            'ownedByTotal',
            'wantedByTotal',
            ['UKRetailPrice', 'priceUK'],
            ['USRetailPrice', 'priceUS'],
            ['CARetailPrice', 'priceCA'],
            ['EURetailPrice', 'priceEU'],
            ['USDateAddedToSAH', 'dateAddedToStore'],
            ['USDateRemovedFromSAH', 'dateRemovedFromStore'],
            'rating',
            'reviewCount',
            'packagingType',
            'availability',
            'instructionsCount',
            'additionalImageCount',
            'EAN',
            'UPC',
            'description',
            'lastUpdated',
        ]

        # Iterate through the XML
        for i in data:
            tag = i.tag.split('}')[-1]

            # Rename the tag if necessary
            try:
                applicableTags.index(tag)
                applicableTags.remove(tag)
            except ValueError:
                for o in applicableTags:
                    if type(o) == list:
                        if tag == o[0]: 
                            tag = o[1]
                            applicableTags.remove(o)
                            break

            # Set the attribute
            setattr(self, tag, i.text)

        # Determine which values haven't been set, and set them to None
        for i in applicableTags:
            tag = i
            if type(i) == list:
                tag = i[1]
            setattr(self, tag, None)

        # Set up tag translations, from one type into another via functions/lambdas
        toInt = lambda x: 0 if x is None else int(x)
        toBool = lambda x: {'true':True,'false':False,'0':False,'1':True}.get(x.lower(), x)
        toDate = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
        translationTags = [
            ['setID', int],
            ['variant', int],
            ['pieces', int],
            ['minifigs', toInt],
            ['reviewCount', toInt],
            ['instructionsCount', toInt],
            ['additionalImageCount', toInt],
            ['released', toBool],
            ['owned', toBool],
            ['wanted', toBool],
            ['rating', float],
            ['ACMDataCount', int],
            ['quantityOwned', int],
            ['dateAddedToStore', toDate],
            ['dateRemovedFromStore', toDate],
            ['lastUpdated', toDate],
        ]

        # Format the tags into the right format
        for i in translationTags:
            x = getattr(self, i[0])
            try:
                setattr(self, i[0], i[1](x))
            except Exception as e:
                pass

        # A simple cache of these items - defaulting to nonexistent
        self._additionalImages = None 
        self._reviews = None
        self._instructions = None


    def __repr__(self):
        return '<{0.__class__.__name__} object with name="{0.name}">'.format(self)


    def getAdditionalImages(self):
        '''
        The same as calling ``client.getAdditionalImages(build.setID)``.

        :returns: A list of URL strings.
        :rtype: list
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
        The same as calling ``client.getReviews(build.setID)``.

        :returns: A list of :class:`brickfront.review.Review` objects.
        :rtype: list
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
        The same as calling ``client.getInstructions(build.setID)``

        :returns: A list of instructions.
        :rtype: list
        '''

        self._instructions = self._client.getInstructions(self.setID)
        return self._instructions


    @property 
    def instructions(self):
        if self._instructions is None:
            self._instructions = self.getInstructions()
        return self._instructions
