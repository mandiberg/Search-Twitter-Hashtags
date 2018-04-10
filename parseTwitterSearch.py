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
thisYear = '2018'

#where the output goes
output = open('output.csv', 'wt')

#where the non-valuable info goes. useful for ensuring you aren't losing any data
slop = open('slop.txt', 'w')
prevLine = ''
myHandle = ''
myDate = ''
myMsg = ''
fullName = ''
lookForYear = False
isRetweet = False
isReply = False
inResults = False
lookForMessage = False
inMessage = False
retweetBody = False
lookForHandle = True
tweetNumber = 0
retweetedHandle = ''
fullNameRetweeted = ''
repliedAuthor = ''
hashtags = ''
retweetMsg = []
startGettingRTMSG = False
try:
	writer = csv.writer(output)
	#here are the titles to the columns in csv file
	writer.writerow(("Tweet Number","Author Handle", "Full Name", "Date", "Message", "Is Retweet", "Is Reply", "Retweeted from Author Handle", "Full Name of Author Retweeted","Retweet Message", "Reply to Author", "Hashtags"))
	for line in allpages:

		handleMatch = re.search(r'(^@[A-Za-z0-9_]+\n)', line)
		lineStripped = line.strip()
		dateMatch = re.search(r'^([A-Z][a-z][a-z]\s[0-9]+)$', lineStripped)
		dateMatchYear = re.search(r'^([0-9]+\s[A-Z][a-z][a-z]\s2?0?1?\d?)$', lineStripped) # line with handle and timestamp with year
		moreMatch = re.search(r'(^More)', lineStripped) # finds 'More' which precedes every tweet body
		replyMatch = re.search(r'([0-9-_\,KM]* rep[A-Za-z]+ [0-9-_\,KM]* retweets? [0-9-_\,KM]* likes?)', lineStripped) # finds the reply/retweet count, which follows every tweet body
		#finds line with handle
		if (lookForHandle and handleMatch):
			myHandle = handleMatch.group().strip()
			fullNameMatch = re.search(r'(^.*?(?=Verified account|\n))', prevLine)
			fullName = fullNameMatch.group().strip()
			print myHandle
			print fullName
			lookForYear = True
		if (lookForYear):
			lookForHandle = False
			if (dateMatch):
				myDate = dateMatch.group() + ' ' + thisYear
			elif (dateMatchYear):
				myDate = dateMatchYear.group()
			# print myDate
			lookForMessage = True #tells code to start looking for tweet body
		if (moreMatch and lookForMessage):
			#finds the "more" at the start of the message, so next lines are the message
			lookForYear = False
			inMessage = True
			retweetLine = 'Retweeted'
			if line.find(retweetLine)!=-1:
				# print "found retweet"
				isRetweet = True
		elif (inMessage is True and not replyMatch):
			if (isRetweet and handleMatch):
				retweetedHandle = handleMatch.group().strip()
				fullNameRetweetedMatch = re.search(r'(^.*?(?=Verified account|\n))', prevPrevLine)
				retweetBody = True
				if(fullNameRetweetedMatch):
					fullNameRetweeted = fullNameRetweetedMatch.group().strip()
#			output.write(line)
			# print ('in the message \r')
			#finds out if this message is a retweet
			hashtagMatch = re.findall(r'(#.[^\s\.]+)', lineStripped)
			if hashtagMatch:
				hashtagMatchesTuple = tuple(hashtagMatch)
				print len(hashtagMatch)
				print hashtagMatchesTuple
				if(hashtags == ''):
					hashtags = " ".join(hashtagMatchesTuple)
					print "empty hashtags"
				else:
					hashtags = hashtags + " " + " ".join(hashtagMatchesTuple)
					print "adding hashtags"

			repliedToMatch = re.search(r'(Replying to (@[A-Za-z0-9_]+))',lineStripped)

			# print retweetMatch
			if re.search(r'(added,\r?\n)',line):
				print "carriage return found"
			if (startGettingRTMSG and (replyMatch is not True)):
				retweetMsg.append(line.strip())
				# print retweetedHandleMatch
				if (retweetBody and not repliedToMatch):

					print fullNameRetweeted
				# elif repliedToMatch:
					# print "replied to found"
			#if this is the first line of msg txt, add line without space at front
			if (myMsg == ''):
				if (repliedToMatch):
					isReply = True
					repliedAuthor = repliedToMatch.group(2)
				myMsg = line
			#if not the first line, add line to existing msg with space in between
			else:
				myMsg = myMsg + ' ' +  line
		elif (replyMatch and inMessage is True):
			#write the data, and clear the variables for the next cycle
			tweetNumber += 1
			writer.writerow( (tweetNumber, myHandle, fullName, myDate , myMsg, isRetweet, isReply, retweetedHandle, fullNameRetweeted, ' '.join(retweetMsg), repliedAuthor, hashtags) )
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
			lookForHandle = True
			retweetBody = False
			retweetMsg = []
			startGettingRTMSG = False

		else:
			#print any line that hasn't been handled here to the slop file
			slop.write(line + '\n')
		if(retweetBody):
			startGettingRTMSG = True
		prevPrevLine = prevLine
		prevLine = line

finally:
    output.close()
