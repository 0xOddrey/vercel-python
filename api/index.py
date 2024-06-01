from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity
model = api.load("glove-twitter-25")

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
		answer = dic['answer']
		answer_vector = model[answer]
		word_vector = model[word]

		# Reshape vectors for cosine similarity calculation
		answer_vector = answer_vector.reshape(1, -1)  # Reshape to row vector
		word_vector = word_vector.reshape(1, -1)    # Reshape to row vector

		# Calculate cosine similarity between "pizza" and the other word
		sim = cosine_similarity(answer_vector, word_vector)[0][0]
		score =  sim * 100
		result = json.dumps({"score": score})
		self.send_response(200)
		self._set_headers()
		self.end_headers()
		self.wfile.write(result.encode())
		return
