This package comes in two parts:
- a REST API written using `flask-restful`; and
- an algorithm that summarizes documents using spaCy and Scikit-Learn.

## How it works

When started, the HTTP server loads a pretrained spaCy model that tokenizes documents sent via POST requests. The sentences in the document are ranked by the weighted frequencies of their constituent words. (This is similar to tf-idf but is limited to one document.) A summary is then assembled from the most important sentences and is returned as a JSON object.

## Requirements

This package has the following dependencies:
- `flask>=1.1.2`;
- `flask-restful>=0.3.8`;
- `scikit-learn>=0.22.1`; and
- `spacy>=2.0.16`.

Additionally, you'll need to download the pretrained spaCy model within a shell session:

```bash
$ python -m spacy download en_core_web_sm
```

Presently, only the English language is supported.

## Usage

In a shell session, run `python api.py` to start up a local HTTP server. You may then send POST requests. The server expects three parameters, all of which are required:
- `"text"`, a Unicode string that contains the (preprocessed) document you wish to summarize;
- `"pct_sentences"`, the percentage of top sentences to include in the summary; and
- `"min_tokens"`, the minimum number of tokens that a sentence must contain for inclusion in the summary.

The server returns a JSON object with a single key, `"summary"`, whose value is an array of the most highly ranked sentences.

Alternatively, you can use the included Dockerfile to build a Docker Image:

```bash
$ docker image build -t summarize-text:latest .
```
Then, run the container like so:

```bash
$ docker run -p 5000:5000 summarize-text:latest
```

This way, you don't have to worry about installing any of the dependencies. Presently, the Image uses the python:3.7-slim image and takes up 445 M.

## Acknowledgements

The extractive text summarization algorithm was forked from Lu&iacute;s Fred's `extractive-text-summarization` repository ([link](https://github.com/luisfredgs/extractive-text-summarization)).
