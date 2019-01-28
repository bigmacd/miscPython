import mechanicalsoup


myNumbers = [
    [ {10, 15, 19, 23, 46 }, { 3 } ],
    [ { 2, 10, 15, 22, 23 }, { 4 } ],
    [ { 1, 14, 11, 19, 23 }, { 1 } ],
    [ { 2,  6,  9, 19, 27 }, { 2 } ],
]


# The key to this dictionary is whether the powerball was matched
prizes = {
    True:
    {
        0: 4,
        1: 4,
        2: 7, 
        3: 100,
        4: 50000, 
        5: "!!!!!!!!!!!!!"
    }, 
    False:
    {
        0: 0,
        1: 0,
        2: 0,
        3: 7, 
        4: 100, 
        5: 1000000
    }
}


def printEntry(prefix: str, entry: list):
    numbers = list(entry[0])
    numbers = sorted(numbers)
    powerball = str(entry[1].copy().pop())
    print(prefix.format(" ".join(str(n) for n in numbers), powerball))


def checkNumbers(currentNumbers: list):
    for number, ticket in enumerate(myNumbers):

        #numbers = list(ticket[0])
        #print ("Checking your numbers: {0} {1}".format(" ".join(str(n) for n in numbers),
        #                                               str(ticket[1].copy().pop())))
        printEntry("Checking your numbers: {0} \tPowerball: {1}", ticket)

        powerballMatch = True if len(ticket[1] & currentNumbers[1]) else False
        matches = len(ticket[0] & currentNumbers[0])
        print("Ticket {0}: won {1}\n".format(number + 1,
                                           prizes[powerballMatch][matches]))


def getNumbers():
    # maybe there are others?
    #url = "https://www.valottery.com/SearchNumbers/powerball/"
    url = "https://www.valottery.com/Data/Draw-Games/powerball"

    # Browser
    browser = mechanicalsoup.Browser(soup_config={ 'features': 'lxml'})

    # The site we will navigate into
    numbersPage = browser.get(url, verify=False)
    # The main section in which we are interested
    panel = numbersPage.soup.find("div", {"class": "right-panel"})
    
    # Output the date for these numbers
    print("\n\nThe current date being checked is: {0}".format(panel.find("h3", { "class": "title-display"}).contents[0]))

    # most recent
    numbers = panel.find("div", {"class": "selected-numbers"})
    b1 = numbers.find("li").contents[0]
    b2 = b1.find_next("li").contents[0]
    b3 = b2.find_next("li").contents[0]
    b4 = b3.find_next("li").contents[0]
    b5 = b4.find_next("li").contents[0]

    powerball  = numbers.find("span", { "id": "bonus-ball-display"}).contents[0]

    retVal = [ { int(b1), int(b2), int(b3), int(b4), int(b5)}, { int(powerball) } ]
    
    # Output what we found
    #print("Current Numbers: {0} {1} {2} {3} {4} {5}".format(b1, b2, b3, b4, b5, powerball))
    printEntry("Current Numbers: {0} \t\tPowerball: {1}\n", retVal)

    return retVal

    


if __name__ == "__main__":
    checkNumbers(getNumbers())
