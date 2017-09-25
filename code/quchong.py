#-*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from operator import itemgetter
import time
import copy

def save_res(res):
    try:
        fp = open("F:\\ss\\py\\taobao\\output_data\\res0316.txt","w+")
        for item in res:
            fp.write(str(item)+"\n")
        fp.close()
    except IOError:
        print("fail to open file")


if __name__ == '__main__':
    file_path = "F:\\ss\\py\\taobao\\output_data\\res.txt"
    r = []
    flag = 0
    for line in open(file_path):
        lines = line.split(" ")
        test_id = lines[0]
        items = lines[1]
        item_id = items.split(",")
        new_item_id = []
        repeat_id = []
        for id in item_id:
            if id not in new_item_id:
                new_item_id.append(id)
            else:
                repeat_id.append(id)
        # func = lambda x, y: x if y in x else x + [y]
        # repeat_id = reduce(func, [[], ] + repeat_id)

        arr = {}
        for i in repeat_id:
            arr[i] = repeat_id.count(i)

        arr = sorted(arr.items(), key=lambda item: item[1], reverse=True)
        new_rep_id = []
        for item in arr:
            new_rep_id.append(item[0])

        res = new_rep_id+new_item_id
        s1 = ','.join(j for j in res)
        s= test_id + " " +s1
        r.append(s)
        flag += 1
    save_res(r)