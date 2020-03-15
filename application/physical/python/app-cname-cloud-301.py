from flask import Flask, request, redirect, make_response, jsonify, has_request_context
from flask.logging import default_handler
import requests
from requests.auth import HTTPBasicAuth
import json
import re
from google.cloud import storage
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

config = {}
workitem = {'source': '', 'target': '', 'configfetchmethod': ''}
storage_client_bucket = 'wbi-gcloud.appspot.com'
bucket_blob = 'config_wbi-gcloud.json'


def readconfig():
    # making a request to an (own) endpoint for future scalability
    urlparts = urlparse(request.url)
    params = {'api_key': 'temp'}
    c = requests.get(urlparts.scheme + '://' + urlparts.netloc +
                     '/api/v1/config',
                     params=params)
    return c.json()


def fetchconfig(methodtype="gcloudstorage", contenttype="json"):
    config = {}

    workitem['configfetchmethod'] = methodtype

    if methodtype == "gcloudstorage" or methodtype is None:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(storage_client_bucket)
        blob = bucket.blob(bucket_blob)
        config = json.loads(blob.download_as_string(client=None))
    elif methodtype == "localfile":
        with open('config_wbi-gcloud.json', 'r') as f:
            config = json.load(f)
    elif methodtype == "inline":
        config = {
            "redirect_urls": [{
                "id": 1,
                "source": "localhost",
                "target": "https://www.google.com"
            }]
        }
    #danger: recursive
    elif methodtype == "endpoint":
        urlparts = urlparse(request.url)
        params = {'api_key': 'temp'}
        config = requests.get(urlparts.scheme + '://' + urlparts.netloc +
                              '/api/v1/config',
                              params=params).json()
    else:
        pass
    return config


@app.before_request
def before_request():
    pass


@app.after_request
def add_header(request):
    #request.headers['X-mytest'] = 'bar'
    request.headers['X-source'] = workitem['source']
    request.headers['X-target'] = workitem['target']
    request.headers['X-configfetchmethod'] = workitem['configfetchmethod']
    return request


@app.route("/api/v1/config", methods=['GET'])
def apiconfigendpoint():
    config = fetchconfig(methodtype="gcloudstorage")
    return jsonify(config)
    #return "error", 500


@app.route("/liveness_check", methods=['GET'])
def liveness_check():
    return "liveness_check"


@app.route("/", methods=['GET'])
def index():
    config = fetchconfig(methodtype="endpoint")

    # parsing the URL into scheme://netloc/path;parameters?query#fragment
    urlparts = urlparse(request.url)
    workitem['source'] = urlparts.netloc

    # now iterating the keys of the dictionary

    for entry in config['redirect_urls']:
        # preparing Pythonesque case-insensitive regex
        pattern = re.compile(entry["source"], re.IGNORECASE)
        if pattern.search(urlparts.netloc):
            # we have a match
            workitem['target'] = entry["target"]
            # performing the HTTP redirect
            return redirect(workitem['target'], code=301)
    return "*.rpasupport.de"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
