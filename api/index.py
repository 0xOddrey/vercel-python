from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def convert_decimal_to_score(decimal):
    """Convert decimal cosine similarity to a custom score."""
    if decimal < 0 or decimal > 1:
        return 1499
    return 1 + (1 - decimal) * (1500 - 1)

class RequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, content_type='application/json'):
        """Set common headers for the response."""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.end_headers()

    def do_OPTIONS(self):
        """Handle options request."""
        self._set_response()
    
    def do_GET(self):
        """Handle GET request."""
        query_components = parse_qs(urlparse(self.path).query)
        word = query_components.get("word", [""])[0].lower()
        corpus = ['swimmer', word]
        
        # Using bi-grams in addition to single words to capture more context.
        tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,2))
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        sim = similarity_matrix[0, 0]
        score = convert_decimal_to_score(sim)
        
        keyWords1 = ["goggles", "olympics", "lanes"]
        keyWords2 = ["water", "pool"]
        bonus = "0"
        if word in keyWords1:
            bonus = '1x'
        elif word in keyWords2:
            bonus = '2x'
        
        result = {"score": score, 'full-score': sim, 'word': word, "bonus": bonus}
        self._set_response()
        self.wfile.write(json.dumps(result).encode('utf-8'))