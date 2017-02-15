import urllib.request as urlrequest
import urllib.error as urlerror
import datetime
from html.parser import HTMLParser

request = urlrequest.Request(
	url="http://www.sudantribune.com/spip.php?rubrique1",
	method="GET",

	)

try:
	response = urlrequest.urlopen(request)
except urlerror.URLErrror as error:
	print("URLError happened: ", error.reason)
	exit(-1)
except urlerror.HTTPError as error:
	print("HTTPError happened: ", error.code)
	exit(-1)

relevant_search_terms = ['econom', 'oil', 'jmec', 'finance', 'budget', 'inflation', 'price']


class WebParser(HTMLParser):

	
	def __init__(self):
		super(WebParser, self).__init__()
		self.found_news = False
		self.news_count = 0
		self.news_relevant_count = 0
		self.news_relevant = False
		self.date_match = False

	def handle_starttag(self, tag, attrs):
		if tag == 'h3':
			self.news_count += 1
			self.found_news = True
			

		if tag == 'abbr':
			# Set a variable with today's date and another one with the desired format
			now = datetime.datetime.now()
			now_formatted = str(now.year) + '-' + str('%02d' % now.month) + '-' + str('%02d' % now.day)

			# Iterate through list of attributes in the abbr tag
			for attr in attrs:
				# If we find the title attribute then we look if today's date matches the published date
				if 'title' in attr:
					self.found_news = True

					if now_formatted in attr[1]:
						self.date_match = True

	def handle_endtag(self, tag):
		self.found_news = False

	def handle_data(self, data):
		if self.found_news and self.date_match:
			#print("News title: ", data)
			for string in data.split():
				if string in relevant_search_terms:
					self.news_relevant_count += 1
					self.news_relevant = True
					print("Relevant news title: ", data)
					break




#Print request response code
print('Response is: ', response)
#Response body is of type bytes so we must cast it into a string for manipulation and parsing later on
response_body = str(response.read())
parser = WebParser()
parser.feed(response_body)
print("In total there were", parser.news_count, "news published in this page")
print("Out of the", parser.news_count, "news published in this page, only", parser.news_relevant_count, "were found to be relevant to our search terms")
