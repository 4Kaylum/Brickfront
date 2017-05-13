class Review(object):
    '''
    A class holding data for a review.

    :ivar author: The `str` name of the person who wrote the review.
    :ivar datePosted: The `str` date that the review was posted.
    :ivar overallRating: The `int` rating that was given.
    :ivar parts: `int`
    :ivar buildingExperience: `int`
    :ivar playability: `int`
    :ivar valueForMoney: `int`
    :ivar title: `str`
    :ivar review: `str`
    :ivar HTML: `bool`
    '''

    def __init__(self, data):
        self.author = data[0].text 
        self.datePosted = data[1].text 
        self.overallRating = int(data[2].text )
        self.parts = int(data[3].text )
        self.buildingExperience = int(data[4].text )
        self.playability = int(data[5].text )
        self.valueForMoney = int(data[6].text )
        self.title = data[7].text
        self.review = data[8].text 
        self.HTML = {
            'true': True,
            'false': False,
            'True': True,
            'False': False,
            '1': True,
            '0': False
        }[data[9].text]
