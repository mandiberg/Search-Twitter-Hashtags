import sys
import re
import csv

'''
This code parses the results of a twitter search into a CSV file.

To generate the twitter data: search a hashtag, scroll down as far as you can, select all then copy and paste that into a text file called input.txt (be sure it is a real text file that strips any formatting). There may be browser add-ons that scroll for you; I just put a piece of walnut(!?!) on my "fn" key, and another on my "down arrow" key, and put something heavy on top and went for a walk. At some point (about 2000 entries for me) the browser starts to slow to a crawl; copy paste at this point, then start the search over at that date using advanced search.

To run: Put input.txt and this file in the same folder run the code in terminal. To get to the directory, type "cd /path/to/directory". To run the code, type "python parseTwitterSearch.py"

Limitations: This is a very simple and rudimentary way of scraping the historical data for a search phrase or hashtag. As it is limited by the manual scraping process, it is possible acquire the data set for 5000 or 10,000, but the manual process becomes too burdensome at some point (e.g. 1,000,000 results). Based on my research, there is no other way to get historical data about a hashtag: all services (including paid subscriptions) only contain 1-2 weeks of data made available via the public API, with the expectation that you want to track a hashtag or phrase going forward into the future. You might be able to automate the screen scraping process via the twitter infinate scroll AJAX to generate the input.txt more seamlessly. It wasn't necessary for my purposes, so I didn't explore it.

The script ignores the difference between original tweets, retweets, and responses.

Reply Tweets begin with a space (e.g. " @username This is my message"). It wasn't necessary to remove this for my purposes.

Written by Michael Mandiberg and licensed under the GPL
'''
# source file - copy your twitter search results into this file
allpages = open('input.txt')

#change this to the current year, as twitter does not display current year in in stamps
thisYear = '2017'

#where the output goes
output = open('output.csv', 'wt')

#where the non-valuable info goes. useful for ensuring you aren't losing any data
slop = open('slop.txt', 'w')

myHandle = ''
myDate = ''
myMsg = ''
fullName = ''
isRetweet = False
isReply = False
inResults = False
lookForMessage = False
inMessage = False
retweetBody = False
tweetNumber = 0
retweetedHandle = ''
fullNameRetweeted = ''
repliedAuthor = ''
hashtags = ''
try:
	writer = csv.writer(output)
	#here are the titles to the columns in csv file
	writer.writerow(("Tweet Number","Author Handle", "Full Name", "Date", "Message", "Is Retweet", "Is Reply", "Retweeted from Author Handle", "Full Name of Author Retweeted", "Reply to Author", "Hashtags"))
	for line in allpages:
		lineStripped = line.rstrip()
		handleMatch = re.search(r'(@[A-Za-z0-9_]+)\s+([A-Z][a-z][a-z])\s+([0-9-_]+)', line) # line with handle and timestamp #FIXME stop catching "@EnisBerberoglu1 and 3 others"
		handleMatchYear = re.search(r'(@[A-Za-z0-9_]+)\s+([0-9-_]+\s+[A-Za-z]+\s+2?0?1?\d?)', line) # line with handle and timestamp with year
		moreMatch = re.search(r'(^More)', line) # finds 'More' which precedes every tweet body
		replyMatch = re.search(r'([0-9-_\,KM]* rep[A-Za-z]+ [0-9-_\,KM]* retweets? [0-9-_\,KM]* likes?)', line) # finds the reply/retweet count, which follows every tweet body
		#finds line with handle and timestamp
		if (handleMatch or handleMatchYear):
			#for current year
			if handleMatch:
#				print 'handleMatch'
				fullNameMatch = re.search(r'(^.*?(?=Verified account|\s@))', line)
				if fullNameMatch:
					fullName = fullNameMatch.group(1).lstrip().rstrip()
				myHandle = handleMatch.group(1)
				myDate = handleMatch.group(3)  + ' ' +  handleMatch.group(2) + ' ' +  thisYear
			#for past years
			elif (handleMatchYear):
#				print ('match with year \r')
				fullNameMatch = re.search(r'(^.*?(?=Verified account|\s@))', line)
				if fullNameMatch:
					fullName = fullNameMatch.group(1).lstrip().rstrip()
				myHandle = handleMatchYear.group(1)
				myDate = handleMatchYear.group(2)
			lookForMessage = True #tells code to start looking for tweet body

		elif (moreMatch and lookForMessage is True):
	#		print(line)
			#finds the "more" at the start of the message, so next lines are the message
			lookForMessage = False
			inMessage = True
		elif (inMessage is True and not replyMatch):
#			output.write(line)
			# print ('in the message \r')
			#finds out if this message is a retweet
			hashtagMatch = re.search(r'(#.[^\s]+)', line)
			if hashtagMatch:
				if(hashtags == ''):
					hashtags = hashtagMatch.group(0)
				else:
					hashtags = hashtags + " " + hashtagMatch.group(0)

			retweetLine = 'Retweeted'
			repliedMatch = re.search(r'(Replying to (@[A-Za-z0-9_]+))',line)
			if line.find(retweetLine)!=-1:
				print "found retweet"
				isRetweet = True
			# print retweetMatch
			if re.search(r'(added,\n)',line):
				retweetBody = True
			if isRetweet:
				retweetedHandleMatch = re.search(r'(\s(@[A-Za-z0-9_]+)\n)', line)
				# print retweetedHandleMatch
				if retweetedHandleMatch and not repliedMatch:
					print 'found retweeted handle'
					fullNameMatchRetweet = re.search(r'(^.*?(?=Verified account|\s@))', line)
					retweetedHandle = retweetedHandleMatch.group(0)
					fullNameRetweeted = fullNameMatchRetweet.group(0)
			#if this is the first line of msg txt, add line without space at front
			if (myMsg == ''):
				if (repliedMatch):
					isReply = True
					repliedAuthor = repliedMatch.group(2)
				myMsg = line
			#if not the first line, add line to existing msg with space in between
			else:
				myMsg = myMsg + ' ' +  line
		elif (replyMatch and inMessage is True):
			#write the data, and clear the variables for the next cycle
			tweetNumber += 1
			writer.writerow( (tweetNumber, myHandle, fullName, myDate , myMsg, isRetweet, isReply, retweetedHandle, fullNameRetweeted, repliedAuthor, hashtags) )
			myHandle = ''
			myDate = ''
			myMsg = ''
			retweetedHandle = ''
			fullNameRetweeted = ''
			repliedAuthor = ''
			hashtags = ''
			isRetweet = False
			isReply = False
			inMessage = False
		else:
			#print any line that hasn't been handled here to the slop file
			slop.write(line + '\n')
finally:
    output.close()
