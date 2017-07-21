# Search-Twitter-Hashtags
This code parses the results of a twitter search into a CSV file

To generate the twitter data: search a hashtag, scroll down as far as you can, select all then copy and paste that into a text file called input.txt (be sure it is a real text file that strips any formatting). There may be browser add-ons that scroll for you; I just put a piece of walnut(!?!) on my "fn" key, and another on my "down arrow" key, and put something heavy on top and went for a walk. At some point (about 2000 entries for me) the browser starts to slow to a crawl; copy paste at this point, then start the search over at that date using advanced search.

To run: Put input.txt and this file in the same folder run the code in terminal. To get to the directory, type "cd /path/to/directory". To run the code, type "python parseTwitterSearch.py"

Limitations: This is a very simple and rudimentary way of scraping the historical data for a search phrase or hashtag. As it is limited by the manual scraping process, it is possible acquire the data set for 5000 or 10,000, but the manual process becomes too burdensome at some point (e.g. 1,000,000 results). Based on my research, there is no other way to get historical data about a hashtag: all services (including paid subscriptions) only contain 1-2 weeks of data made available via the public API, with the expectation that you will track a hashtag or phrase going forward into the future. You might be able to automate the screen scraping process via the twitter infinate scroll AJAX to generate the input.txt more seamlessly. It wasn't necessary for my purposes, so I didn't explore it.

In its initial form, the script ignores the difference between original tweets, retweets, and responses. We are trying to revise that now.

Reply Tweets begin with a space (e.g. " @username This is my message"). It wasn't necessary to remove this for my purposes.

Written by Michael Mandiberg and licensed under the GPL
