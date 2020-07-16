from flask import Flask, jsonify
from flask_restful import Api, reqparse, Resource
import spacy
from summarize import summarize

app = Flask(__name__)
api = Api(app)
nlp = spacy.load("en_core_web_sm")

class SummarizeText(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("text", required=True)
        self.parser.add_argument("pct_sentences", required=True, type=float)
        self.parser.add_argument("min_tokens", required=True, type=int)
        super(SummarizeText, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        doc = nlp(args.text)
        summary = summarize(doc, args.pct_sentences, args.min_tokens)
        return jsonify(summary=summary)

api.add_resource(SummarizeText, "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
