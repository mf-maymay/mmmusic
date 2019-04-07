# -*- coding: utf-8 -*-
from functools import reduce
from utils import get_artist_name, get_related


def escape_special_chars(string):
    char_list = ("$",)
    replaced = string
    for char in char_list:
        replaced = replaced.replace(char, "\\" + char)
    return replaced


ids = {
    "akron family": "64l9cD8tQscYZCGRLlNm3f",
    "alice coltrane": "0oKYiTD5CdNbrofRvM1dIr",
    "american football": "5FwydyGVcsQllnM4xM6jw4",
    "andrew bird": "4uSftVc3FPWe6RJuMZNEe9",
    "andrew bird's bowl of fire": "0Dan4711eVqYQnlUWfOvYN",
    "azizi gibson": "2NjfafEappzvGGGDdMRJMP",
    "beach house": "56ZTgzPBDge0OvCGgMO3OY",
    "ben frost": "6qEM4txXHvfMbOUOK9L7pl",
    "black sabbath": "5M52tdBnJaKSvOpJGz8mfZ",
    "blonde redhead": "5isqImG0rLfAgBJSPMEVXF",
    "bob marley": "2QsynagSdAqZj3U9HgDzjD",
    "candiria": "2HlW9aXquEwJ3ywGlPEUPp",
    "chelsea wolfe": "6ZK2nrW8aCTg8Bid7I7N10",
    "claude debussy": "1Uff91EOsvd99rtAupatMP",
    "cocteau twins": "5Wabl1lPdNOeIn0SQ5A1mp",
    "creedence clearwater revival": "3IYUhFvPQItj6xySrBmZkd",
    "cultura profetica": "65HuWBUC1d8ty1q6J42Nfi",
    "dan deacon": "5Z3IWpvwOvoaWodujHw7xh",
    "daughters": "1LhK7wn59Hq6GNN4sUS3ih",
    "david bowie": "0oSGxfWSnnOXhD2fKuz2Gy",
    "death grips": "5RADpgYLOuS2ZxDq7ggYYH",
    "deerhoof": "7AZwAitWq1KcFoIJhRWb6V",
    "denzel curry": "6fxyWrfmjcbj5d12gXeiNV",
    "deradoorian": "3jLCHiuXBTGEEku37TsobP",
    "dexys midnight runners": "4QTVePrFu1xuGM9K0kNXkk",
    "dirty three": "1QUsHFoDqNsC0W9AlNyHWF",
    "dr octagon": "7dr3cSEOIZ6tBrm4y1wsnr",
    "drive like jehu": "7FbdCzKUwoZs1v9bCl43Ev",
    "d'angelo": "336vr2M3Va0FjyvB55lJEd",
    "earl sweatshirt": "3A5tHz1SfngyOZM2gItYKu",
    "electric wizard": "4htjQW3lgIwL6fEJlTOez4",
    "erykah badu": "7IfculRW2WXyzNQ8djX8WX",
    "failure": "3grvcGPaLhfrD5CYsecr4j",
    "faust": "4yBBNmdvVaoPEnr2lt14q7",
    "fiona apple": "3g2kUQ6tHLLbmkV7T4GPtL",
    "fire orchestra": "50BFEG33gYorCS5zbNbLRb",
    "flatbush zombies": "1dqGS5sT6PE2wEvP1gROZC",
    "foxing": "2dfxY7YDuYCUtWFzWTS6IR",
    "frank sinatra": "1Mxqyy3pSjf8kZZL4QVxS0",
    "flying lotus": "29XOeO6KIWxGthejQqn793",
    "gospel": "7uqOQ6QYdmLuF6NklBYdiY",
    "have a nice life": "0FRKTwQSToXpCxYMhyUzYY",
    "hella": "1n861RIk6CTAWncgHR9UHg",
    "hiatus kaiyote": "43JlwunhXm1oqdKyOa2Z9Y",
    "iceage": "03hlOXqRyyXO3ectp3eEbU",
    "isis": "2vsXeWGC8rILp3rpSN2Fyk",
    "jambinai": "20xwrwSmGSBQLLV0EVRS9M",
    "james blake": "53KwLdlmrlCelAZMaLVZqU",
    "jimi hendrix": "776Uo845nYHJpNaStv1Ds4",
    "joey badass": "2P5sC9cVZDToPxyomzF1UH",
    "ka": "0cmqAB0gdr6ObvjNrQJAQr",
    "kamasi washington": "6HQYnRM4OzToCYPpVBInuU",
    "kanye west": "5K4W6rqBFWDnAN6FQUkS6x",
    "kendrick lamar": "2YZyLoL8N0Wb9xBt1NhZWg",
    "king crimson": "7M1FPw29m5FbicYzS2xdpi",
    "king krule": "4wyNyxs74Ux8UIDopNjIai",
    "larry young": "6Y6kAZs0W9NNsxNbpImPvq",
    "led zeppelin": "36QJpDe2go2KgaRleHCDTp",
    "liars": "2z78AlkdwE2Ghj9EB50M6z",
    "lightning bolt": "2og3FOCLYXT9H7IYE6QPUq",
    "little dragon": "6Tyzp9KzpiZ04DABQoedps",
    "magazine": "4VuMnSnoTGrma3a79UhfMs",
    "mammal hands": "497rp5TEzJffeBnUT0BeE1",
    "mf doom": "2pAWfrd7WFF3XhVt9GooDL",
    "mia doi todd": "1r3efMZ0kcejkPKP8oQZzv",
    "miles davis": "0kbYTNQb4Pb1rPbbaF0pT4",
    "milo": "0J6PhnVD21GSFoJ9HoadLH",
    "modest mouse": "1yAwtBaoHLEDWAnWR87hBT",
    "mogwai": "34UhPkLbtFKRq3nmfFgejG",
    "moodie black": "3rd7jOmgOraHucrcvhYVy6",
    "moses sumney": "5W10uJRsbt9bROJDKoI1Wn",
    "mouse on the keys": "6NVzd3Lv9yMFIf1bsXNLIp",
    "nai palm": "5X0dCi2aVnYEV27S8wgQdF",
    "nina simone": "7G1GBhoKtEPnP86X2PvEYO",
    "nirvana": "6olE6TJLqED3rqDCT0FyPh",
    "owls": "57sqenSxpn1IL2G0im58dj",
    "oxbow": "4m47y2u5lJBKbakAv5YAh1",
    "parquet courts": "23NIwARd4vPbxt3wwNnJ6k",
    "picastro": "1TTJJzHdc6IWChZrVpkr4k",
    "pretend": "4rohfx5aI2ISAXUkFXPy9R",
    "radiohead": "4Z8W4fKeB5YxbusRsdQVPb",
    "robert johnson": "0f8MDDzIc6M4uH1xH0o0gy",
    "roberto musci": "1HSz5qiRNcs8eJ0Sp2LOxw",
    "rockets red glare": "0w0bmTGF2xge5DzAQQXj61",
    "ryuichi sakamoto": "1tcgfoMTT1szjUeaikxRjA",
    "sangre de muerdago": "31B0gbLzmTRdprWvyq5S2y",
    "santana": "6GI52t8N5F02MxU0g5U69P",
    "seasick steve": "6OVkHZQP8QoBYqr1ejCGDv",
    "shellac": "6I8R5MFTlez7rHCsH4cx0u",
    "signor benedick": "3vA9OkEhOskFChlPRkoGQz",
    "skinny puppy": "5Mu0EMEsUIVE132pNMywns",
    "slint": "4IwOItqRhsIoRuD5HP4vyC",
    "stan getz": "0FMucZsEnCxs5pqBjHjIc8",
    "steely dan": "6P7H3ai06vU1sGvdpBwDmE",
    "sun ra": "0tIODqvzGUoEaK26rK4pvX",
    "swans": "79S80ZWgVhIPMCHuvl6SkA",
    "swell maps": "1FGzeqDPTLZwfbfxpmPAZn",
    "sylvan esso": "39vA9YljbnOApXKniLWBZv",
    "tera melos": "3K4vimkwmCyjD4g1hEMPjZ",
    "terry riley": "7DnLQaXsqcYkgm0nyDrB3r",
    "the avalanches": "3C8RpaI3Go0yFF9whvKoED",
    "the sea and cake": "0ihBDeJlIlXo4LFfAllsGm",
    "the strokes": "0epOFNiUfyON9EYx7Tpr6V",
    "the third eye foundation": "1C4Ix8pbUGqzAP79elcpcm",
    "the upsetters": "12CNljuN6DW9e5x61FS03b",
    "there will be fireworks": "4z5OpKj6xIhU18pxrTKfCj",
    "thom yorke": "4CvTDPKA6W06DRfBnZKrau",
    "three 6 mafia": "26s8LSolLfCIY88ysQbIuT",
    "throbbing gristle": "1UYhxPY1oqFUg1HfF8nV3k",
    "unwound": "4YjpqCSDD7zwMQgPYJMqb0",
    "vince staples": "68kEuyFKyqrdQQLLsmiatm",
    "warpaint": "3AmgGrYHXqgbmZ2yKoIVzO",
    "wire": "2i8ynmFv4qgRksyDlBgi6d",
    "wu-tang clan": "34EP7KEpOjXcM2TCat1ISk",
    "xxxtentacion": "15UsOTVnJzReFVN1VCnxy4"
}


class Finder(object):
    ids = ids

    def __init__(self, *artist_kws, artist_ids=None):
        self.artist_kws = artist_kws

        self.artist_ids = [ids[artist_kw] for artist_kw in artist_kws]

        if artist_ids is not None:
            self.artist_ids.extend(artist_ids)

        self.artist_names = {k: get_artist_name(k) for k in self.artist_ids}

        self.sets = {k: {k} for k in self.artist_ids}

        self.edges = set()

        self.lasts = {k: s.copy() for k, s in self.sets.items()}

    def expand(self):
        for k in self.artist_ids:
            new = set()
            for artist in self.lasts[k]:
                add = {related["id"] for related in get_related(artist)}
                self.edges |= {(artist, related) for related in add}
                new |= add
            self.lasts[k] = new - self.sets[k]
            self.sets[k] |= self.lasts[k]

    def find(self):
        # TODO: Consider changing condition for greater numbers of artists.
        while not self.midpoints(names=False):
            self.expand()

    def midpoints(self, names=True):
        if names:
            return sorted(map(get_artist_name, self.midpoints(names=False)))
        else:
            return reduce(set.intersection, self.sets.values())


if __name__ == "__main__":
    finder = Finder("death grips", "earl sweatshirt")
