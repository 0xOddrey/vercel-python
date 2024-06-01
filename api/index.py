from http.server import BaseHTTPRequestHandler
from urllib import parse
import numpy as np
import json
import gensim.downloader as api
from http import HTTPStatus

# Download and load the pre-trained Word2Vec model
print("Loading model...")
model = api.load("glove-twitter-25")
print("Model loaded.")

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
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()

    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

        # Debugging info
        print("Received request with query parameters:", dic)

        if "word" not in dic or "answer" not in dic:
            self.send_response(HTTPStatus.BAD_REQUEST)
            self._set_headers()
            self.wfile.write(json.dumps({"error": "Missing 'word' or 'answer' parameter"}).encode())
            return

        word = dic["word"]
        answer = dic["answer"]

        try:
            answer_vector = model[answer]
            word_vector = model[word]
            sim = cosine_similarity(answer_vector, word_vector)
            score = sim * 100
            result = json.dumps({"score": score})
            self.send_response(HTTPStatus.OK)
            self._set_headers()
            self.wfile.write(result.encode())
        except KeyError as e:
            self.send_response(HTTPStatus.BAD_REQUEST)
            self._set_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        except Exception as e:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self._set_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())