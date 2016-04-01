from gensim import corpora, models, similarities
from gensim.models import ldamodel
import string
import os
import sys
import re
import nltk, xml, xml.etree.ElementTree as xtree
# nltk.download()
from nltk.corpus import stopwords
from bs4 import BeautifulSoup, SoupStrainer
list1 =[]

stoplist=stopwords.words('english')
stoplist.append('a')
stoplist.append('<a')
stoplist.append('i.e.')
stoplist=["a", "<a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", 
"because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", 
"besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", 'i.e.',
"cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", 
"down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", 
"etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", 
"fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", 
"front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", 
"hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", 
"hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", 
"latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", 
"mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", 
"neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", 
"now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", 
"otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", 
"same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", 
"since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", 
"somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", 
"then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", 
"thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", 
"to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", 
"up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", 
"whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", 
"which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", 
"without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "advertisement"]

str1 = ""
with open ("wiki_00.xml",'r') as f:
	str1= f.read()
	for link in BeautifulSoup(str1, parse_only=SoupStrainer('a')):
		
		for words in link.text.split(" "):
			if words not in stoplist:
				list1.append(words)

listSubDocs=(str1.split("===="))

for doc in listSubDocs:
	doc.translate(None, string.punctuation)


texts = [[word for word in document.lower().split() if word not in stoplist and word in list1]
          for document in listSubDocs]

from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
	for token in text:
		if 'href=' not in token and '</a>' not in token and '<a' not in token:
			if token.translate(None, string.punctuation):
				frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1 ]
          for text in texts]



dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') 


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) 
# print str(corpus)


tree = xtree.parse("wiki_00.xml")

xmlRoot = tree.getroot()
child = xtree.Element("num_features")
child.text=str(len(dictionary.keys()))
child1= xtree.Element("corpus")
child1.text = str(corpus)
xmlRoot.append(child)
xmlRoot.append(child1)

tree.write("wiki_01.xml")


