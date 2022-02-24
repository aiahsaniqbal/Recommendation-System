# Import the libraries
import time
import pandas as pd
from liberty_functions import get_item_detail, get_item_title, clean_item_title
from flask import jsonify
from timeit import default_timer as timer
import logging

global_start_time = time.time()


def filter_dict(df_input, d, current_item_title,identifier,attribute_1):
    ''' Filters dictionary d by removing items with same item title as the current item. '''
    new_dict = {}
    item_names = [clean_item_title(current_item_title.lower())]
    # print(clean_item_title(current_item_title))
    for key, value in d:
        # Is condition satisfied?
        this_item_title = clean_item_title(get_item_title(df_input, value,identifier,attribute_1)).lower()
        # print("Key:(", this_item_title, ") Value:(", str(current_item_title).strip(), ")")
        # if this_item_title not in item_names:
        if True:
            # print(str(get_item_title(df_input, value)).strip())
            item = {key: value}
            new_dict.update(item)
            item_names.append(this_item_title)

    return new_dict


def recommend(item_id, num_items, df_input, results_input, identifier,attribute_1,attribute_2, debug=False):
    ''' Recommend items similar to the current item. '''
    # global df, results, filtered_results
    ts = timer()
    # logging.info('Recommending items for ID:{}'.format(item_id))
    item_recom_list = {}
    # if not df_input.empty:
        # print("Is existing df empty? ", df.empty)
    # df = df_input
        # logging.debug("using df parameter")

    # if len(results_input) > 0:
        # print("Is existing results empty? ", results[0])
    # results = results_input
        # logging.debug("using results parameter")

    try:
        # logging.debug('filtering results')
        filtered_results = results_input[int(item_id)][:int(num_items) + 20]
        # 20 additional items are added to accomodate duplicate removal process
    except:
        # logging.debug('error filtering results')
        filtered_results = {}  # item not found

    if len(filtered_results) == 0:
        # logging.info('item ID not found')
        # return {item_id: "item ID not found"}
        return None

    current_item_title = get_item_title(df_input, item_id,identifier,attribute_1)
    filtered_results = filter_dict(df_input, filtered_results, current_item_title,identifier,attribute_1)
    filtered_results = sorted(filtered_results.items(), key=lambda x: -x[0])[:int(num_items)]
    # logging.debug('Compiling content item recommendations')
    for rec in filtered_results:
        if debug:
            name_score = get_item_detail(df_input, rec[0],identifier,attribute_1,attribute_2) + ' - (score: ' + str(round(rec[1], 4)) + ')'
            item = {str(rec[0]): name_score}
        else:
            item = {int(rec[0]): float(round(rec[1], 4))}
        item_recom_list.update(item)
        # print(get_item_detail(df, rec[1]) + " (score:" + str(round(rec[0], 4)) + ")")

    tf = (timer() - ts).__round__(4)
    #logging.debug("Exec time: " + str(tf) + " s")
    if not debug:
        item_recom_list={k: v for k, v in sorted(item_recom_list.items(), key=lambda item: item[1],reverse=True)}
    return item_recom_list


