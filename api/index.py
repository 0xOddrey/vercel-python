from http.server import BaseHTTPRequestHandler
from urllib import parse
import spacy

nlp = spacy.load("en_core_web_sm")

def convert_decimal_to_score(decimal):
    if decimal < 0 or decimal > 1:
        return 1499
    
    return 1 + (1 - decimal) * (1500 - 1)


class handler(BaseHTTPRequestHandler):

	def do_GET(self):
		s = self.path
		dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
		word = dic["word"]
		word = word.lower()
		sim = nlp('shark').similarity(nlp(word))
		score = convert_decimal_to_score(sim)

		self.send_response(200)
		self.send_header('Content-type','text/plain')
		self.end_headers()
		message = str(score)
		self.wfile.write(message.encode())
		return