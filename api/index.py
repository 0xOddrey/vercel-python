from http.server import BaseHTTPRequestHandler
from urllib import parse
import spacy
import json
from PyDictionary import PyDictionary
dictionary=PyDictionary()

nlp = spacy.load("en_core_web_sm")

def convert_decimal_to_score(decimal):
	if decimal < 0 or decimal > 1:
		return 1499
	
	return 1 + (1 - decimal) * (1500 - 1)

class handler(BaseHTTPRequestHandler):

	def _set_headers(self):
		self.send_header('Content-Type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
		self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
		self.send_header('Access-Control-Allow-Headers', 'Content-Type')


	def do_OPTIONS(self):
		self.send_response(200)
		self._set_headers()
		self.end_headers()


	def do_GET(self):
		s = self.path
		dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
		word = dic["word"]
		word = word
		answer = dict['answer']
		answer = answer
		full_word = "%s - %s" % (word, dictionary.meaning(word))
		full_answer = "%s - %s" % (answer, dictionary.meaning(answer))
		print(full_word)
		print(full_answer)
		sim = nlp(full_answer).similarity(nlp(full_word))
		score = convert_decimal_to_score(sim)
		result = json.dumps({"score": score})
		self.send_response(200)
		self._set_headers()
		self.end_headers()
		self.wfile.write(result.encode())
		return