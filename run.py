#!/usr/bin/env python

import json
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
import logging
import sys
import resources  # our classes for processing book requests
import nltk
nltk.download('stopwords')

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='service_log.log', filemode='a', format='%(levelname)s:%(asctime)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
app.logger.disabled = False
logging = logging.getLogger('werkzeug')
logging.disabled = True
_host = ""
_port = ""


# @app.before_request
# def before_request():
#     content = request.json
#     app.logger.debug(content)


@app.after_request
def after_request(response):
    #app.logger.debug('Response: ' + response.status + ', ' + response.data.decode('utf-8'))
    return response


def init_config():
    global _host, _port
    try:
        logger.info('.................. App Starting and Logging Enabled..................')
        app.logger.debug('Initializing config')
        app.config["JSON_SORT_KEYS"] = False  # Keep visual sort order so that json results show in scored order
        api_config = json.load(open("routes.json"))
        global _host, _port, _datapath, _fileext  # , df, results
        # Map classes to APIs
        app.logger.debug('Mapping classes')
        api.add_resource(resources.ContentBasedRecommendItem, api_config['ContentBasedRecommendItem'])
        app.logger.debug('Setting up host, port, datapath and fileext')

        _host = api_config['hostname']
        _port = api_config['portnum']
        resources._datapath = api_config['datapath']
        resources._fileext = api_config['fileext']

        resources.display_attribute_1 = api_config['display_attribute_1']
        resources.display_attribute_2 = api_config['display_attribute_2']
        resources.file_csv = api_config['file_csv']
        resources.identifier = api_config['identifier']


        resources.display_attribute_1_second = api_config['display_attribute_1_second']
        resources.display_attribute_2_second = api_config['display_attribute_2_second']
        resources.file_csv_second = api_config['file_csv_second']
        resources.identifier_second = api_config['identifier_second']

        app.logger.debug('Host: ' + str(_host))
        app.logger.debug('Port: ' + str(_port))




    except:
        logging.exception("Exception : ",
                          "Error @ PostResponse! " + str(sys.exc_info()[0]) + " occured. " + str(sys.exc_info()[1]))


# if __name__ == '__main__':
_host = ""
_port = 0
feature_1=feature_2=file_1=file_2=output_file=identifier_1=identifier_2=''
init_config()
app.run(host=_host, port=_port, debug=False)

