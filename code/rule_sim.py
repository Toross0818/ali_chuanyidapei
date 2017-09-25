#-*- coding: UTF-8 -*-
import pandas as pd
import time


def cos(tset_name,dim_name):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    vector1 = [int(i) for i in tset_name.split(',')]
    vector2 = [int(i) for i in dim_name.split(',')]
    vector1.sort()
    vector2.sort()
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        res_arr=0.0
    else:
        res_arr = (dot_product / ((normA*normB)**0.5))
    return res_arr

def save_res(res):
    try:
        fp = open("F:\\ss\\py\\taobao\\output_data\\0318\\res.txt","w+")
        for item in res:
            fp.write(str(item)+"\n")
        fp.close()
    except IOError:
        print("fail to open file")


def sim(res_item_data,item_not_matched):
    flag = 0
    time1 = time.clock()
    res_arr = []
    for test_item in res_item_data[:2].iterrows():
        flag+=1
        test_id = test_item[1]['item_id']
        test_term_name = test_item[1]['term_name']
        cos_dic = {}
        for dim_item in item_not_matched.iterrows():
            item_id = dim_item[1]['item_id']
            item_name = dim_item[1]['term_name']
            sim_cos = cos(test_term_name, item_name)
            cos_dic[item_id] = sim_cos
        cos_dic = sorted(cos_dic.items(), key=lambda item: item[1], reverse=True)
        res_id = [int(i[0]) for i in cos_dic[:200]]
        s1 = ','.join(str(j) for j in res_id)
        s = str(test_id) + " " + s1
        print s
        res_arr.append(s)
        time2 = time.clock()
        print str(flag)+" "+"time：%f" %(time2-time1)
    return res_arr

if __name__ == '__main__':
    matchsets_file = "F:\\ss\\py\\taobao\\input_data\\dim_fashion_matchsets.txt"
    item_file = "F:\\ss\\py\\taobao\\input_data\\dim_items.txt"
    user_bought_file = "F:\\ss\\py\\taobao\\input_data\\user_bought_history.txt"
    test_item_file = "F:\\ss\\py\\taobao\\input_data\\test_items.txt"

    bought_data = pd.read_table(user_bought_file, sep='\s+', names=['user_id', 'item_id', 'create_at']).drop(
        ['create_at', 'user_id'], axis=1).drop_duplicates()
    bought_data['flag'] = 1
    dim_items = pd.read_table(item_file, sep='\s+', names=['item_id', 'cat_id', 'term_name'])
    dim_items = dim_items[dim_items['term_name'].notnull()]
    print dim_items
    new_dim_index=[]
    for item in dim_items.iterrows():
        index = item[0]
        term_name = item[1]['term_name']
        if len(term_name.split(","))>4:
            new_dim_index.append(index)
    dim_items = pd.DataFrame(dim_items, index=new_dim_index)

    test_item_data = pd.read_table(test_item_file, sep='\s+', names=['item_id'])
    test_bought_data = pd.merge(bought_data, test_item_data, on="item_id", how='right')
    test_not_bought = test_bought_data[test_bought_data['flag'].isnull()]
    res_item_data = pd.merge(dim_items, test_not_bought, on='item_id', how='inner').drop(['flag'],axis=1)
    dim_fashion_matchs = pd.read_table(matchsets_file, sep='\s+', names=['coll_id', 'item_list'])
    item_id = []
    for items in dim_fashion_matchs['item_list']:
        for item in items.split(";"):
            for id in item.split(","):
                item_id.append(int(id))
    item_matched = pd.DataFrame(item_id).rename(columns={0: "item_id"}).drop_duplicates()
    item_matched['flag'] = 1
    item_not_matched = pd.merge(item_matched, dim_items, on='item_id', how='right')
    item_not_matched = item_not_matched[item_not_matched['flag'] != 1].drop(['flag'], axis=1)
    test_item_data = pd.read_table(test_item_file, sep='\s+', names=['item_id'])
    test_item_data['flag'] = 1
    item_not_matched = pd.merge(item_not_matched, test_item_data, on='item_id', how='left')
    item_not_matched = item_not_matched[item_not_matched['flag'] != 1].drop(['flag'], axis=1)

    print'开始计算相似度...'
    res_arr = sim(res_item_data,item_not_matched)
    save_res(res_arr)
