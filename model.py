import requests
import json
import spacy
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer 
from spacy.lookups import Lookups
from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_lg")

class TempestEngine(object):
	def __init__(self, url):
		self.queries = []
		self.replies = []
		self.intents = []
		self.url = url

	def get_json_url(self):
		sheet_id = self.url.split('/')[5] # id at 5th index
		new_url = "https://spreadsheets.google.com/feeds/cells/{}/1/public/full?alt=json".format(sheet_id)

		return new_url

	def get_knowledge_graph(self):
		json_url = self.get_json_url(self.url)

		res = requests.get(json_url)
		text = res.content.decode("utf-8")
		api_content = json.loads(text)
		content = api_content['feed']['entry']

		for i in range(0, len(content), 3):
			q = content[i]['content']['$t']
			r = content[i+1]['content']['$t']
			i = content[i+2]['content']['$t']

			self.queries.append(q)
			self.replies.append(r)
			self.intents.append(i)

		self.queries = self.queries[1:]
		self.replies = self.replies[1:]
		self.intents = self.intents[1:]

	def clean_query(self, query):
		tokens = nltk.word_tokenize(query)
		# remove stop words

		# lematize all words
		lemmatizer = WordNetLemmatizer()
		lemmas = ' '.join([lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens])

		return lemmas

	def find_similarity(self, query):
		query_tokens = nlp(query)
		sim_score = []
		for query in self.queries:
			comp_tokens = nlp(query)
			sim_score.append(np.abs(query_tokens.similarity(comp_tokens)))

		sim_score = np.array(sim_score)

		return sim_score

	def get_query_reply(self, query):
		sim = self.find_similarity(query)

		index = np.argmax(sim)
		return self.replies[index]

		def get_wordnet_pos(self, word):
			"""Map POS tag to first character lemmatize() accepts"""
			tag = nltk.pos_tag([word])[0][1][0].upper()
			
			tag_dict = {"J": wordnet.ADJ,
					"N": wordnet.NOUN,
					"V": wordnet.VERB,
					"R": wordnet.ADV}

			return tag_dict.get(tag, wordnet.NOUN)		

	def find_pos(self, query):
		tokens = nltk.word_tokenize(query)
		pos_tag_tokens = nltk.pos_tag(tokens)
		return pos_tag_tokens