import mechanicalsoup


myNumbers = [
    [ {10, 15, 19, 23, 46 }, { 3 } ],
    [ { 2, 10, 15, 22, 23 }, { 4 } ],
    [ { 1, 14, 11, 19, 23 }, { 1 } ],
    [ { 2,  6,  9, 19, 27 }, { 2 } ],
]


def checkNumbers(currentNumbers: list):
    for number, ticket in enumerate(myNumbers):
        powerballMatch = True if len(ticket[1] & currentNumbers[1]) else False
        matches = len(ticket[0] & currentNumbers[0])
        msg = "{0} the powerball".format("and" if powerballMatch else "but not")
        print("Ticket {0} has {1} match{2} {3}".format(number + 1, 
                                                       matches, 
                                                       "" if matches == 1 else "es", 
                                                       msg))


def getNumbers():
    # maybe there are others?
    url = "https://www.valottery.com/SearchNumbers/powerball/"

    # Browser
    browser = mechanicalsoup.Browser(soup_config={ 'features': 'lxml'})

    # The site we will navigate into
    numbersPage = browser.get(url, verify=False)

    # most recent
    b1 = numbersPage.soup.find("td", { "class": "whiteball"}).contents[0]
    b2 = b1.find_next("td", { "class": "whiteball"}).contents[0]
    b3 = b2.find_next("td", { "class": "whiteball"}).contents[0]
    b4 = b3.find_next("td", { "class": "whiteball"}).contents[0]
    b5 = b4.find_next("td", { "class": "whiteball"}).contents[0]
    powerball  = numbersPage.soup.find("td", { "class": "redball"}).contents[0]

    
    return [ { int(b1), int(b2), int(b3), int(b4), int(b5)}, { int(powerball) } ]


if __name__ == "__main__":
    checkNumbers(getNumbers())