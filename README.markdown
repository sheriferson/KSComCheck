# KSComCheck

![](kscc.png)

[KSComCheck][] is a utility that will notify you of the latest comments posted on Kickstarter projects that you want to follow.

[KSComCheck]: newurlsoon

KSComCheck relies on [terminal-notifier][] for notifications, and so it only works on OS X. It will check against the last comment it saw, and notify you if the newest comment it just fetched is different.

[terminal-notifier]: https://github.com/julienXX/terminal-notifier

![](screenshot.png)

## Installation and usage

To install `terminal-notifier`:

``` bash
$ brew install terminal-notifier
```

Until I find a better way of handling dependencies so you don't have to, the script also needs the following python modules

- [ BeautifulSoup4 ](http://www.crummy.com/software/BeautifulSoup/)
- [ requests ](http://docs.python-requests.org/en/latest/)

``` bash
$ pip install BeautifulSoup4 requests
```

Finally, tell KSComCheck which projects you want to be notified about by listing them (giving them a one-word name) along with the links to their comments pages in `projects.conf`:

```
[projects]
courg = https://www.kickstarter.com/projects/reduxwatch/redux-courg-hybrid-watches-with-missions-to-tackle/comments
ember = https://www.kickstarter.com/projects/842978788/ember-equipment-modular-urban-pack/comments
```

Now give it a test run:
``` bash
$ python KSComCheck.py
```

### Run on a schedule

KSComCheck works best when run on a schedule. You can use whatever scheduling system you want to use. I use and recommend [LaunchControl][9034-0001], a [launchd](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html) GUI app.

[9034-0001]: http://www.soma-zone.com/LaunchControl/ "soma-zone: LaunchControl"


### Known issues

KSComCheck could hang if run within [tmux][5946-0001]. This is related to how [terminal-notifier][] works. See issue [#115](https://github.com/julienXX/terminal-notifier/issues/115), and especiallly [this comment](https://github.com/julienXX/terminal-notifier/issues/115#issuecomment-104214742) on a possible fix involving [`reattach-to-user-namespace`][5946-0002].

[5946-0001]: https://tmux.github.io/ "tmux"
[5946-0002]: https://github.com/ChrisJohnsen/tmux-MacOSX-pasteboard "ChrisJohnsen/tmux-MacOSX-pasteboard · GitHub"


## Background

Some Kickstarter projects have very active comments pages.

These comments aren't useless; they will often have very valuable information that is revealed or decided by the project creators during the funding phase, or valuable information shared by other backers, and that information is sometimes not communicated successfully to people not actively following the comments sections.

There is no way for you to ask Kickstarter to notify you of comments posted to the project. Kickstarter also -- unfortunately -- has no public API, so I have to resort to web scraping (If anyone from KS is reading, I hope you don't mind.)

## Personal note

I would appreciate any and all constructive criticism about how to make the code or project better.
If you see something in the code or structure that make you think _"wtf?"_ I want to hear about it!
Please take the time to tell me.

_"You wanna be a true friend to them? Be honest, and unmerciful."_ -- [Lester Bangs][am]

[am]: http://www.imdb.com/title/tt0181875/

## License

``` text
The MIT License (MIT)

Copyright (c) 2015 Sherif Soliman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Icon

I made the icon in about 10 minutes using [Michael Flarup][]'s incredible [App Icon Template][].

[Michael Flarup]: http://www.pixelresort.com/
[App Icon Template]: http://appicontemplate.com/

## To do

- [ ] Add tests
- [ ] Add launchservices plist and instructions for scheduling
- [ ] Improve comment detection to detect number of new comments since last check
