import pickle
import pandas as pd
from flask import jsonify, request
from flask_restful import Resource, reqparse
import book_recommend_linear_kernel_read
import random

import logging
import os
import json
import time

df = pd.DataFrame
final = final_book = books = similarity_with_book = sim_user_30_item = book_user = Mean = pd.DataFrame
results = {}
display_attribute_1=display_attribute_2=identifier=''
display_attribute_1_second=display_attribute_2_second=identifier_second=""
'''*****Loggings'''
with open("log_config.json", "r") as jsonfile:
    log_keys = json.load(jsonfile)


def log_Key_Based(key_log="", value_log="", separator_log=True):
    '''---> Concatenates key,=,key. Keys are defined in log_config'''
    if separator_log:#---> checks if separator is needed or it's last value in Log message
        return log_keys.get(key_log) + '=' + log_keys.get(value_log) + log_keys.get('Separator')
    else:
        return log_keys.get(key_log) + '=' + log_keys.get(value_log)


def log_Value_Based(key_log="", value_log="", separator_log=True):
    '''---> cancatenates key, =, value. Keys are defined in log_config'''
    if separator_log:#---> checks if separator is needed or it's last value in Log message
        return log_keys.get(key_log) + '=' + str(value_log) + log_keys.get('Separator')
    else:
        return log_keys.get(key_log) + '=' + str(value_log)


def logging_parameters(flag_debug, resource_type, product_id, search_results, retrieval_mode, status_response, message_response, start_time):
    if (flag_debug):
        logging.info(
            log_Key_Based('Debug Mode', 'On') + log_Key_Based('Recommendation Types', resource_type) + log_Value_Based("User ID",
                                                                                                                       product_id) + log_Value_Based(
                "Number of Results", search_results) +
            log_Key_Based('Retrieval Mode', retrieval_mode) + log_Value_Based('Status Code', status_response) + log_Key_Based('Message', message_response) + log_Value_Based(
                'Execution Time', str((time.time() - start_time).__round__(4)) + 's', False))
    else:
        logging.info(
            log_Key_Based('Debug Mode', 'Off') + log_Key_Based('Recommendation Types', resource_type) + log_Value_Based("User ID",
                                                                                                                        product_id) + log_Value_Based(
                "Number of Results", search_results) +
            log_Key_Based('Retrieval Mode', retrieval_mode) + log_Value_Based('Status Code', status_response) + log_Key_Based('Message',
                                                                                                                              message_response) + log_Value_Based(
                'Execution Time', str((time.time() - start_time).__round__(4)) + 's', False))




class ContentBasedRecommendItem(Resource):

    def post(self):
        global df, results
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int, required=True, nullable=False)
        parser.add_argument('num_items', type=int, required=False, store_missing=True, default=20, nullable=True)
        parser.add_argument('debug', type=str, required=False, nullable=True)
        parser.add_argument('search_type', type=str, required=True, nullable=False)

        args = parser.parse_args(strict=True)
        num_items = int(args["num_items"])
        search_type = str(args["search_type"])
        self.condition_check(search_type)
        search_type=""

        # logging.info('Content: Item ID:{}, Num Results:{}'.format(args['item_id'], args['num_items']))
        # print(type(args['debug']), args['debug'])
        if (args['debug'] == "True" or args['debug'] == "true"):
            flag_debug = True
        else:
            flag_debug = False

        if (num_items < 1 or num_items > 100):
            msg = "Please enter any value between 1-30 for 'num_items'"
            response = jsonify({"status": 101, "message": msg, "data": None})
            status_response = 101
            message_response = "Enter Value Between 1-30"
            logging_parameters(flag_debug, 'Content Based', args['item_id'], args['num_items'],
                               'Manually Curated Results',
                               status_response, message_response, start_time)
            return response
        else:
            data = book_recommend_linear_kernel_read.recommend(int(args["item_id"]), int(args["num_items"]),
                                                               self.df, self.results, self.identifier,self.display_attribute_1,self.display_attribute_2,flag_debug)
            if (data is not None):
                # print(data)
                response = jsonify({"status": 100, "message": "success", "data": data})
                status_response = 100
                message_response = "Success"
                logging_parameters(flag_debug, 'Content Based', args['item_id'], args['num_items'],
                                   'Normal Retrieval',
                                   status_response, message_response, start_time)
                return response
            else:
                msg = "Item ID not found'"
                response = jsonify({"status": 102, "message": msg, "data": None})
                status_response = 102
                message_response = msg
                logging_parameters(flag_debug, 'Content Based', args['item_id'], args['num_items'],
                                   'Item ID Not Found',
                                   status_response, message_response, start_time)

                df = None
                results = None

                return response

    def get(self):
        return self.post()

    def condition_check(self,search_type):
        global df, results, _datapath, _fileext, start_time, file_csv, display_attribute_1, display_attribute_2, \
            identifier, file_csv_second, display_attribute_1_second, display_attribute_2_second, identifier_second

        # search_type='company'

        if(search_type=='c'):
            file_csv_new=file_csv_second
            disp_att_1=display_attribute_1_second
            disp_att_2 =display_attribute_2_second
            identi=identifier_second
        elif (search_type=='t'):
            file_csv_new = file_csv
            disp_att_1 = display_attribute_1
            disp_att_2 = display_attribute_2
            identi = identifier


        # if df.empty:
            # logging.debug('Reading item data from csv')
            # df = pd.read_csv('LibertyBooks-GoodReadsReviews-Clean.csv')
        df = pd.read_csv(file_csv_new)
        start_time = time.time()

        # if not results:
            # logging.debug("reading results dictionary from file path: {}".format(_datapath))
        files = [i for i in os.listdir(_datapath) if i.endswith(_fileext)]
        for file in files:
            # logging.debug("reading file: {}".format(file))
            with open(file, 'rb') as f:
                temp_res = pickle.load(f)
                results = {**results, **temp_res}  # merge both dictionaries
            f.close()
            # with open('book_recommendation_results_0_19999.npy', 'rb') as f:
            #     results = pickle.load(f)
            # f.close()
            # logging.debug("Serving {} item matches today...".format(len(results)))
        if(search_type=='c'):
            # change file
            results=self.change_npy_form(results)

        self.df = df
        self.results = results
        self.display_attribute_1 = disp_att_1
        self.display_attribute_2 = disp_att_2
        self.identifier = identi



    @staticmethod
    def change_npy_form(out_put):

        dic = {}
        id_1 = []
        id_2 = []
        sim = []
        for value in out_put.keys():
            for item in out_put[value]:
                id_1.append(value)
                id_2.append(item[0])
                sim.append(item[1])
                # print(str(value)+" : "+str(temp[0])+" : "+str(temp[1]))
        # print(str(id_1) + " : " + str(id_2) + " : " + str(sim))
        import numpy as np
        id_new_2 = np.unique(np.array(id_2)).tolist()
        dic = dic.fromkeys(id_new_2)
        for key in dic.keys():
            dic[key] = []
        for idx, i in enumerate(id_2):
            dic[i].append((id_1[idx], sim[idx]))
        # print(out_put)
        # print(dic)
        return dic

    def __init__(self):
        global df, results, _datapath, _fileext, start_time,file_csv, display_attribute_1,display_attribute_2, \
            identifier,file_csv_second,display_attribute_1_second,display_attribute_2_second,identifier_second
        # logging.debug('Initializing ContentBasedRecommendItem class')
        start_time = time.time()



# http://127.0.0.1:7000/item_recommend/content_based_rec_item?num_items=100&search_type=companyy&item_id=817
#