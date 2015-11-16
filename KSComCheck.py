# KSComCheck.py
# Show notifications for new comments posted on Kickstarter
# projects of interest.
# Sherif Soliman
# sherif@ssoliman.com

import bs4
import ConfigParser
import hashlib
import os.path
import pickle
import requests
from subprocess import call

# get the real path to the directory where
# this script is living
pathToMe = os.path.realpath(__file__)
pathToMe = os.path.split(pathToMe)[0]

pathToPickle = os.path.join(pathToMe, "latesthash.p")
pathToLogo = os.path.join(pathToMe, "kscc.png")

def readProjectLinks():
    """
    This function will look for the projects.conf file and parse it to
    get the projects and their corresponding comments links.
    
    It will save those in projects{}
    """
    config = ConfigParser.ConfigParser()
    if os.path.isfile('projects.conf'):
        config.readfp(open('projects.conf'))

    projects = {}
    try:
        projectItems = config.items("projects")
        # tip for this solution found here:
        # http://stackoverflow.com/a/8048529
        for project, link in projectItems:
            projects[project] = link
    except:
        # this is bad error handling
        # on my list to improve in the future
        print "An error occurred while parsing the projects.conf file."
        print "Make sure it is formatted properly."
        quit

    return projects

def getLatestCommentAndAuthorForProjects(projects):
    """
    getLatestCommentAndAuthorForProjects(projects)

    projects : dictionary with project name as key, comments link as value

    Will parse the projects dictionary, which contains
    project names and their respective links, and download the html
    for each projects.
    It will then call parseProjectHTML() to get the author and comment.

    Will then add them to respective dictionaries.

    Returns:
    - projectLatestAuthors{project: author}
    - projectLatestComments{project: comment}
    
    """

    projectLatestAuthors = {}
    projectLatestComments = {}

    if len(projects) > 0:
        try:
            for project in projects.keys():
                link = projects[project]
                request = requests.get(link)
                bsSoup = bs4.BeautifulSoup(request.text, 'lxml')
                author, comment = parseProjectHTML(bsSoup)
                projectLatestAuthors[project] = author
                projectLatestComments[project] = comment
        except:
            print "An error occurred while trying to download the comments."
            quit

    return projectLatestAuthors, projectLatestComments

def parseProjectHTML(ksoup):
    """
    parseProjectHTMLs(ksoup)

    Handed some soup from bs4.BeautifulSoup(request.text, 'lxml')

    Parses and soup and returns the author and comment
    """
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

    return author, latestComment

def checkForNewCommentsandNotify(projectComments, projectAuthors, projectLinks):
    """
    checkForNewCommentsandNotify(projectComments, projectAuthors)

    Handed:
    projectComments{project: latestComment}
    projectAuthors{project: author}
    projectLinks{project: link}

    Cycles through the projects and checks to see if there are saved comments.
    Checks to see if the latest comments are different than the saved ones.
    Sends a notification if the latest comment that is fetched is new.

    """
    # check to see if the pickle file exists
    # if it does, read what is inside
    if os.path.isfile(pathToPickle):
        try:
            savedHashDict = pickle.load(open(pathToPickle))
            if type(savedHashDict) is not dict:
                raise ValueError("Saved file possibly corrupt.")

        except:
            print "There was a problem with loading saved data."
            print "Deleting the old save state and starting fresh."
            os.remove(pathToPickle)
            savedHashDict = {}
    else:
        savedHashDict =  {}

    for project in projectComments.keys():
        comment = projectComments[project]

        # hash the comment in prep for comparison
        latestCommentHash = hashlib.sha1(comment).hexdigest()

        # is the latest comment different than the saved one?
        if project not in savedHashDict.keys() or latestCommentHash != savedHashDict[project]:
            # noify the user
            try:
                call("/usr/local/bin/terminal-notifier -message '" + comment + \
                        "' -title '\[" + project + " project] " + projectAuthors[project] +  "' " + \
                        "-appIcon '" + pathToLogo + "' " + \
                        "-open '" + projectLinks[project] + "'" \
                        , shell = True)
            except:
                print "An error occurred while trying to notify you of a new comment."
                print "Are you sure you have terminal-notifer installed? Check the README."

            savedHashDict[project] = latestCommentHash

        pickle.dump(savedHashDict, open(pathToPickle, "wb"))

if __name__ == "__main__":
    projectAuthors = {}
    projectComments = {}
    # what projects do you want to stay updated on?
    projectLinks = readProjectLinks()
    # what are the latest comments on those project, and who are the authors?
    projectAuthors, projectComments = getLatestCommentAndAuthorForProjects(projectLinks)
    # have you been notified of these comments before?
    checkForNewCommentsandNotify(projectComments, projectAuthors, projectLinks) 
