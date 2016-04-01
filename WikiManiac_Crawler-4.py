#Wikipedia Crawler v3 (inserting results into MySQL)
# @author: Vijaya R Singh, Aqib Bhat, Abhishek

#Import Libraries
import time     #For Delay
import urllib.request    #Extracting web pages
import re
import json
import os.path
import sys
import random



#Defining pages
starting_page = "George_Clooney"
seed_page = "https://en.wikipedia.org"  #Crawling the English Wikipedia

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
	textdata = ""
		
	def handle_starttag(self, tag, attrs):
		pass
	def handle_endtag(self, tag):
		pass
	def handle_data(self, data):
		self.add_data(data)
		
	def add_data(self, data):
		self.textdata += " " + data
		
	def get_data(self):
		return self.textdata
		
	def clear_text(self):
		self.textdata = ""


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
	try:
		headers = {}
		headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
		req = urllib.request.Request(url, headers = headers)
		resp = urllib.request.urlopen(req)
		respData = str(resp.read().decode('utf-8'))

		#print(type(respData))
		js=json.loads(respData)
		#print(js)
		final_raw_html = js["query"]["pages"][list(js["query"]["pages"].keys())[0]]["extract"]
		return final_raw_html
	except Exception as e:
		print(str(e))

#Extract all the links
#Finding 'Next Link' on a given web page
def get_next_link(s):
	start_link = s.find("<a href")
	if start_link == -1:    #If no links are found then give an error!
		end_quote = 0
		link = "no_links"
		return link, end_quote
	else:
		start_quote = s.find('"', start_link)
		end_quote = s.find('"',start_quote+1)
		link = str(s[start_quote+1:end_quote])
		return link, end_quote
		  

#Getting all links with the help of 'get_next_links'
def get_all_links(url2):
	try:
		headers = {}
		headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
		links = []
		req2 = urllib.request.Request(url2, headers = headers)
		resp2 = urllib.request.urlopen(req2)
		respData2 = str(resp2.read().decode('utf-8'))
		js2=json.loads(respData2)
		pages = js2["query"]["pages"]
		for key in pages.keys():
			links.append(pages[key]["title"])
		return links 
	except Exception as e:
		print(str(e))

t0 = time.time()
database = {}   #Create a dictionary
count = 0


#Main Crawl function that calls all the above function and crawls the entire site sequentially
def web_crawl():  
	try:
		to_crawl = [starting_page]      #Define list name 'Seed Page'
		#print(to_crawl)
		parser = MyHTMLParser()
		crawled={}      #Define list name 'Seed Page'
		#database = {}   #Create a dictionary
		#k = 0;
		for k in range(0, 3):
			i=0        #Initiate Variable to count No. of Iterations
			while True:     #Continue Looping till the 'to_crawl' list is not empty
				urll = to_crawl.pop(0)      #If there are elements in to_crawl then pop out the first element
				
				
					
					  
				if urll in crawled.keys():     #Else check if the URL is already crawled
						pass        #Do Nothing
				else:       #If the URL is not already crawled, then crawl i and extract all the links from it

						url_for_content = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&titles=" + urll.replace(' ', '_')

						raw_html = download_page(url_for_content)
						#print(raw_html)
						if raw_html!=None:
							parser.feed(raw_html)
							content = parser.get_data()

							global count
							#Writing the output data into a text file
							if content != None and content != "":
								page_title = 'page_' + urll.replace(' ', '_')
								page1 = os.path.join('./crawled_pages',page_title+".txt")
								file = open(page1, 'w')        #Open the text file called database.txt
								file.write(content + "\n\n")      #write the introduction of that page
								file.close()                            #Close the file
								parser.clear_text()
								count+=1

							if count > 100001:
								import csv
								w = csv.writer(open("output.csv", "w"))
								for key, val in crawled.items():
								    w.writerow([key, val])
								f_out_crawled = open('crawled.txt', 'w')
								f_out_crawled.write(str(crawled))
								f_out_crawled.close()
								print("crawled list saved")
								print("============== 100000 documents downloaded === Leave me alone now !! ==================")
								sys.exit(0)
							print(count)
							time.sleep(0.75)
						#print("Link = " + urll)
						
						#raw_html = download_page(urll)
						#print(raw_html)
						
						get_links_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=" + urll + "&generator=links&gpllimit=max"
						
						next_links = get_all_links(get_links_url)
						if next_links != None:
							to_crawl = to_crawl + next_links
						#print(to_crawl)

						crawled[urll] = 1
						
		
						#Remove duplicated from to_crawl
						n = 1
						j = 0
						#k = 0
						while j < (len(to_crawl)-n):
							if to_crawl[j] in to_crawl[j+1:(len(to_crawl))]:
								to_crawl.pop(j)
								n = n+1
							else:
								pass     #Do Nothing
							j = j+1
				i=i+1
				#print(i)
				#print(k)
				#print(to_crawl)
				#print("Iteration No. = " + str(i))
				#print("To Crawl = " + str(len(to_crawl)))
				#print("Crawled = " + str(len(crawled)))
	except:
		import csv
		w = csv.writer(open("output.csv", "w"))
		for key, val in crawled.items():
			w.writerow([key, val])
		f_out_crawled = open('crawled.txt', 'w')
		f_out_crawled.write(crawled)
		f_out_crawled.close()
		print("crawled list saved")
	return ""

print (web_crawl())

t1 = time.time()
total_time = t1-t0
print(total_time)
