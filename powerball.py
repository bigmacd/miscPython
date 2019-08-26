import os
import mechanicalsoup
from gmail import Gmail
from datetime import datetime, timedelta
import time
import encodings.idna

myNumbers = [
    [ {10, 15, 19, 23, 46 }, { 3 } ],
    [ { 2, 10, 15, 22, 23 }, { 4 } ],
    [ { 1, 14, 11, 19, 23 }, { 1 } ],
    [ { 2,  6,  9, 19, 27 }, { 2 } ]
]

outputMessage = ""

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

def Print(msg):
    global outputMessage
    outputMessage += msg
    outputMessage += "\n"


def printEntry(prefix: str, entry: list):
    numbers = list(entry[0])
    numbers = sorted(numbers)
    powerball = str(entry[1].copy().pop())
    Print(prefix.format(" ".join(str(n) for n in numbers), powerball))


def checkNumbers(currentNumbers: list):
    for number, ticket in enumerate(myNumbers):

        #numbers = list(ticket[0])
        #print ("Checking your numbers: {0} {1}".format(" ".join(str(n) for n in numbers),
        #                                               str(ticket[1].copy().pop())))
        printEntry("Checking your numbers: {0} \tPowerball: {1}", ticket)

        powerballMatch = True if len(ticket[1] & currentNumbers[1]) else False
        matches = len(ticket[0] & currentNumbers[0])
        if powerballMatch == True:
            Print ("Powerball matches!")
        Print ("Matched {0} numbers".format(matches))
        Print("Ticket {0}: won {1}\n".format(number + 1,
                                             prizes[powerballMatch][matches]))


def getNumbers():
    # maybe there are others?
    #url = "https://www.valottery.com/SearchNumbers/powerball/"
    url = "https://www.valottery.com/Data/Draw-Games/powerball"

    # Browser
    browser = mechanicalsoup.Browser(soup_config={ 'features': 'lxml'})

    # The site we will navigate into
    numbersPage = browser.get(url) #, verify=False)
    # The main section in which we are interested
    panel = numbersPage.soup.find("div", {"class": "right-panel"})

    # Output the date for these numbers
    Print("The current date being checked is: {0}".format(panel.find("h3", { "class": "title-display"}).contents[0]))

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


def timeToWakeUp():
    # if it is around just past midnight on Thursdays(3) or Sundays(6), go ahead and run
    dayOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    retVal = False
    sleepTime = 0
    n = datetime.now()
    print("found weekday = {0}, hour is: {1}".format(dayOfWeek[n.weekday()], n.hour))

    whereIam = (n.weekday() * 24) + n.hour
    if whereIam == 72:
        retVal = True
        sleepTime = 72
    elif whereIam == 144:
        retVal = True
        sleepTime = 96
    elif whereIam < 72:
        sleepTime = 72 - (whereIam)
    elif whereIam < 144:
        sleepTime = 144 - (whereIam)
    else:
        sleepTime = (168 - (whereIam)) + 72
    #if n.weekday() == 3 or n.weekday() == 6:
    #    if n.hour == 0:
    #        retVal = True
    return retVal, sleepTime


if __name__ == "__main__":
    while True:
        print("checking if it is time to wake up...")
        isTime, sleepHours = timeToWakeUp()
        if isTime:
            outputMessage = ""
            print ("waking up!")
            checkNumbers(getNumbers())

            g = Gmail()
            g.setFrom('martin.cooley@gmail.com')
            g.addRecipient('martin.cooley@gmail.com')
            g.subject("Do you want to be a milli?")
            g.message(outputMessage)
            username = os.environ['username']
            appkey = os.environ["appkey"]
            g.setAuth(username, appkey)
            g.send()
        print ("sleeping for {0} hours".format(sleepHours))
        time.sleep(sleepHours * 60 * 60)
