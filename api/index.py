from http.server import BaseHTTPRequestHandler
from urllib import parse
import spacy
import json


nlp = spacy.load("en_core_web_sm")

def convert_decimal_to_score(decimal):
	if decimal < 0 or decimal > 1:
		return 1499
	
	return 1 + (1 - decimal) * (1500 - 1)

class handler(BaseHTTPRequestHandler):

	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT')
		self.send_header('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version')
		self.end_headers()


	def do_GET(self):
		s = self.path
		dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
		word = dic["word"]
		word = word.lower()
		sim = nlp('swimmer').similarity(nlp(word))
		score = convert_decimal_to_score(sim)
		keyWords1 = ["goggles", "olympics", "lanes"]
		keyWords2 = ["water", "pool"]
		bonus = "0"
		if word in keyWords1:
			bonus = '1x'
			score = min(score * 1.2, 50)
		if word in keyWords2:
			bonus = '2x'
			score = min(score * 2, 20)
			
		result = json.dumps({"score": score, 'full-score': sim, 'word': word, "bonus": bonus})
		self.send_response(200)
		self.send_header('Content-type','text/plain')
		self.end_headers()
		self.wfile.write(result.encode())
		return