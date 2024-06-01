from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import gensim
import numpy as np
import gzip
import shutil
import gensim.downloader as api
import os

model_path = "./glove-wiki-gigaword-50.gz"
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

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
		answer = dic["answer"]
		answer_vector = model[answer]
		word_vector = model[word]
		sim = cosine_similarity(answer_vector, word_vector)
		sim = sim * 100
		result = json.dumps({"score": sim})
		self.send_response(200)
		self._set_headers()
		self.end_headers()
		self.wfile.write(result.encode())
		return