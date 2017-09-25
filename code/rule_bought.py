#-*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from operator import itemgetter
import time
import copy


if __name__ == '__main__':
    user_bought_file = "F:\\ss\\py\\taobao\\input_data\\user_bought_history.txt"
    test_item_file = "F:\\ss\\py\\taobao\\input_data\\test_items.txt"
    matchsets_file = "F:\\ss\\py\\taobao\\input_data\\dim_fashion_matchsets.txt"
    item_file = "F:\\ss\\py\\taobao\\input_data\\dim_items.txt"
    # dim_fashion_matchs = pd.read_table(matchsets_file, sep='\s+', names=['coll_id', 'item_list'])
    # dim_items = pd.read_table(item_file, sep='\s+', names=['item_id', 'cat_id', 'term_name'])
    # dim_items = dim_items[dim_items['term_name'].notnull()]
    # print dim_fashion_matchs
    # print dim_items
    bought_data = pd.read_table(user_bought_file, sep='\s+', names=['user_id', 'item_id', 'create_at'])
    # print  bought_data.sort(['create_at'])
    bought_data_11_12 = bought_data[(bought_data['create_at']==20141111)| (bought_data['create_at']==20141212)]
    print bought_data_11_12
    test_item_data = pd.read_table(test_item_file, sep='\s+', names=['item_id'])
    test_bought_data = pd.merge(bought_data_11_12, test_item_data, on="item_id", how='inner')
    test_item_id = test_bought_data[['item_id']].drop_duplicates()
    print test_item_id

    test_user_id = test_bought_data.drop(['item_id'], axis=1).drop_duplicates()

    test_ui_data = pd.merge(bought_data, test_user_id, on='user_id', how='inner').reset_index()
    print test_ui_data
    items = []
    n = 0
    for i, j in test_ui_data.groupby([test_ui_data['user_id']]):
        item = list(j['item_id'])

        items.append(item)
    r = []
    flag = 0
    for test_id in test_item_id.values[:, :].tolist():
        flag += 1
        # arr = []
        s1 = str(test_id[0])
        s2 = ''
        for i in items:
            if test_id in i:
                i.remove(test_id)
                s2 += ','.join(str(j) for j in i)
        s = s1 + " " + s2
        print s
        r.append(s)
        print flag
    time2 = time.clock()
    # save_res(r)
    # print "time:%f" % (time2 - time1)