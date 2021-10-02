from elasticsearch import Elasticsearch
import os

client = Elasticsearch(
	hosts=[os.environ.get("ES_HOST", 'locahost')], # for local instance
	http_auth=['elastic', os.environ.get('ES_PWD')]
	)
