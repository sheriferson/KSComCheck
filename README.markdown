# KSComCheck

![](screenshot.png)

KSComCheck is an OS X python utility that will notify you of the latest comment posted on a Kickstarter project that you're following.

If you run it on a schedule (say using [launchd](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html)) it will check against the last comment it saw, and notify you if the newest comment it just fetched is different.

KSComCheck relies on [`terminal-notifier`](https://github.com/julienXX/terminal-notifier) to post notifications on OS X.

To install `terminal-notifier`:

```
brew install terminal-notifier
```

Until I find a better way of handling dependencies so you don't have to, the script also needs the following python modules

- BeautifulSoup4
- requests

```
pip install BeautifulSoup4 requests
```

This is the very first commit. The utility checks only one project's comments page, and that one project is hardcoded in the script. It's a minimal working script. Improvements to follow.

## Background

Some Kickstarter projects have very active Comments pages. One that is currently in its manufacturing phase has accumulated over 2,000 comments.

These comments aren't useless; they will often have very valuable information that is revealed or decided by the project creators during the funding phase, or valuable information shared by other backers, and that information is sometimes not communicated successfully to people not actively following the comments sections.

There is no way for you to ask Kickstarter to notify you of comments posted to the project. Kickstarter also -- unfortunately -- has no public API, so I have to resort to web scraping (If anyone from KS is reading, I hope you don't mind.)

