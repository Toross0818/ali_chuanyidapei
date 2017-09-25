#-*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from operator import itemgetter
import time
import copy

def save_res(res):
    try:
        fp = open("F:\\ss\\py\\taobao\\output_data\\0320\\0320_3.txt","w+")
        for item in res:
            fp.write(str(item)+"\n")
        fp.close()
    except IOError:
        print("fail to open file")

if __name__ == '__main__':
    file_path1 = "F:\\ss\\py\\taobao\\output_data\\0320\\0320_2.txt"
    file_path2 = "F:\\ss\\py\\taobao\\input_data\\ronghe\\sim.csv"

    history_data = pd.read_table(file_path1, sep='\s+', names=['item_id', 'items_list'])

    sim_data = pd.read_table(file_path2, sep='\s+', names=['item_id', 'sim_items_list'])
    his_sim_not_same = pd.merge(sim_data,history_data,on=['item_id'],how='left')
    his_sim_not_same = his_sim_not_same[his_sim_not_same['items_list'].isnull()].drop(['items_list'],axis=1).rename(columns={'sim_items_list':'items_list'})
    #融合
    res = [his_sim_not_same,history_data]
    res = pd.concat(res)
    res_arr=[]
    for dim_item in res.iterrows():
        item_id = dim_item[1]['item_id']
        item_name = dim_item[1]['items_list']
        s = str(item_id) + " " +item_name
        res_arr.append(s)
    save_res(res_arr)