from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
count_vect = CountVectorizer()

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

		corpus = ['swimmer',word]

		vectorizer = TfidfVectorizer()
		trsfm=vectorizer.fit_transform(corpus)
		result = cosine_similarity(trsfm[0:1], trsfm)
		sim = result[0][1]
		score = convert_decimal_to_score(sim)
		keyWords1 = ["goggles", "olympics", "lanes"]
		keyWords2 = ["water", "pool"]
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