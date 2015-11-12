# KSComCheck.py
# Show notifications for new comments posted on Kickstarter
# projects of interest.
# Sherif Soliman
# sherif@ssoliman.com

import bs4
import hashlib
import os.path
import pickle
import requests
from subprocess import call

# get the real path to the directory where
# this script is living
pathToMe = os.path.realpath(__file__)
pathToMe = os.path.split(pathToMe)[0]

# link to favourite project's comments page
ksURL = "https://www.kickstarter.com/projects/reduxwatch/redux-courg-hybrid-watches-with-missions-to-tackle/comments"

# get the html of the page
ksHTML = requests.get(ksURL)

# parse the HTML using Beautiful Soup
# and create a bs object
ksoup = bs4.BeautifulSoup(ksHTML.text, 'lxml')

# find all the comments.
# at this point coms will be a list of 50 elements
coms = ksoup.findAll('div', {'class': 'main clearfix pl2 ml2'})

# the latest comment will contain two <p> elements
# one for the author, one for the comment
# get the second paragraph of the latest comment
parsInLatest = coms[0].findAll('p')

# we'll get the author some other way
# right now author information is in an <a> tag
linksInLatest = coms[0].findAll('a')
author = linksInLatest[0].getText()

# construct the comment string by concatenating
# all the <p> tags we found
latestComment = ""
for ii in range(len(parsInLatest)):
    if latestComment == "":
        latestComment += parsInLatest[ii].getText()
    else:
        latestComment += "\n" + parsInLatest[ii].getText()

# replace single quote characters with wrapped quotation marks
# so it can survive the bash gauntlet
# see http://stackoverflow.com/q/1250079
# otherwise terminal-notifier will only show text
# up to the first single quote
latestComment = latestComment.replace("'", "\'\"\'\"\'")

# get a SHA1 hash of the latest comment text
latestCommentHash = hashlib.sha1(latestComment).hexdigest()

# notify the user of the latest comment text
# and pickle the new hash

pathToPickle = os.path.join(pathToMe, "latesthash.p")
pathToLogo = os.path.join(pathToMe, "kslogo.png")

def handleNewLatestComment():
    """
    This function will be called if the code has determined that
    the latest fetched comment is newer than the previously stored
    latest comment.

    It will call `terminal-notifier` to show a notification,
    and will pickle the hash of the latest fetched comment.
    """

    call("/usr/local/bin/terminal-notifier -message '" + latestComment + \
            "' -title '" + author + "' " + \
            "-appIcon '" + pathToLogo + "' " + \
            "-open '" + ksURL + "'" \
            , shell = True)
    pickle.dump(latestCommentHash, open(pathToPickle, "wb"))

# first check if there _is_ a stored hash
if os.path.isfile(pathToPickle):
    # if the hash file exists, unpickle/load it and check
    # it against latest current
    latestStoredHash = pickle.load(open(pathToPickle))
    
    if latestStoredHash != latestCommentHash:
        handleNewLatestComment()

# else: didn't find a pickle file
else:
    handleNewLatestComment()

