from http.server import BaseHTTPRequestHandler
from urllib import parse
import spacy
import json


nlp = spacy.load("en_core_web_md")

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
		word = dic.get("word", "").lower()
		print(word)
		sim = nlp('gymnast').similarity(nlp(word))
		score = convert_decimal_to_score(sim)
		keyWords1 = ["chalk", "olympics", "flip"]
		keyWords2 = ["routine", "dismount"]
		bonus = "0"
		if word in keyWords1:
			bonus = '1x'
		if word in keyWords2:
			bonus = '2x'
		result = json.dumps({"score": score, "bonus": bonus})
		self.send_response(200)
		self._set_headers()
		self.end_headers()
		self.wfile.write(result.encode())
		return