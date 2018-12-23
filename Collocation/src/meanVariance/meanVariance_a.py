import os
import json

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store results
dict_res = {}
doc = list(os.listdir(rootdir))

def text_process(text, dist):
    single_npair = []
    with open(text, 'r', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            proc_sentence = []
            for word in sentence:
                temp = word.split('/')
                if temp[1] != 'w':
                    word = temp[0]
                    proc_sentence.append(word)
            if dist >= 0:           
                for pos in range(len(proc_sentence) - 1):
                    if pos + dist < len(proc_sentence):
                        single_npair.append((proc_sentence[pos], proc_sentence[pos + dist]))
            else:
                for pos in range(len(proc_sentence) - 1)[::-1]:
                    if pos + dist >= 0:
                        single_npair.append((proc_sentence[pos], proc_sentence[pos + dist]))
    return single_npair

# nebor frequence calc
def fre_calculate(curtext, dict):
    for pair in curtext:
        if not dict.__contains__(pair):
            dict[pair] = 1
            # dict_pair.update({pair : 1})
        else:
            dict[pair] += 1

def filter_result(dict, judge):
    filtresult = []
    sorted_res = sorted(dict.items(), key = lambda k: k[1])
    for i in reversed(sorted_res):
        # print(i[1], type(i[1]))
        if i[1] > judge:
            filtresult.append(i)
    return filtresult

def filter_result_list(dict, judge):
    filtresult = []
    sorted_res = sorted(dict.items(), key = lambda k: sum(k[1]))
    for i in reversed(sorted_res):
        # print(i[1], type(i[1]))
        if sum(i[1]) > judge:
            filtresult.append(i)
    return filtresult

def tuple_toDic(curfretext):
    temp_lookup = {}
    for curpair in curfretext:
        pair = curpair[0]
        value = curpair[1]
        if not temp_lookup.__contains__(pair):
            temp_lookup[pair] = value
    return temp_lookup

def freq_analysis(pairdict, dist):
    for pair in dict_res:
        if pairdict.__contains__(pair[0]):
            dict_res[pair].insert(dist, pairdict[pair[0]])
        else:
            dict_res[pair].insert(dist, 0)

"""
def distance_frequence(curpair, step):
    '''
    :type pair: tuple
    '''
    pair = curpair[0]
    value = curpair[1]
    if not dict_res.__contains__(pair):
        dict_res.update({pair : [value]})
    elif step == 0:
        return
    else:
        for i in range(len(doc)):
            tmp_pair = {}
            step_res = text_process(rootdir + doc[i], step)
            fre_calculate(step_res, tmp_pair)
            if tmp_pair.__contains__(pair):
                # dict_res[pair] += tmp_pair[pair]
                dict_res[pair].append(tmp_pair[pair])
            else:
                # dict_res[pair] += 0
                dict_res[pair].append(0)
"""

def dist_proc(distance, frefilter):
    # store result of frequences of nebor pairs
    dict_pair = {}
    for i in range(len(doc)):
        fre_calculate(text_process(rootdir + doc[i], distance), dict_pair)
    dist_res = filter_result(dict_pair, frefilter)
    return dist_res

def main():
    with open(resdir + '2_a_100.txt', 'w', encoding='gbk') as res:
        # dict_pair = {}
        for i in doc:
            if i == '.DS_Store':
                doc.remove(i)
        """
        for i in range(len(doc)):
            fre_calculate(text_process(rootdir + doc[i], 1), dict_pair)
        one_res = filter_result(dict_pair, 100)
        """
        one_res = dist_proc(1, 100)
        original = tuple_toDic(one_res)
        for pair in original:
            if not dict_res.__contains__(pair):
                dict_res.update({pair: [original[pair]]})

        for step in range(-5, 0):
            cur_res = tuple_toDic(dist_proc(step, 0))
            freq_analysis(cur_res, step)
        for step in range(5, 10):
            cur_res = tuple_toDic(dist_proc(step, 0))
            freq_analysis(cur_res, step)
        filter_result_list(dict_res, 100)

        # print(sorted(dict_res))
        # print(dict_res)
        """
        sorted_dres = sorted(dict_res, key = lambda k: k[1][-1])
        for i in sorted_dres:
            res.write(' '.join(str(t) for t in i) + '\n')
        """
        
        for k, v in dict_res.items():
            res.write(str(k) + ', ' + str(v) + '\n')
        
        """  
        for pair in dict_res:
            if original.__contains__(pair[0]):
                dict_res[pair].insert(1, original[pair[0]])
            else:
                dict_res[pair].insert(1, 0)
        """
        # print(dict_res)

        """   
        for i in dict_pair:
            distance_frequence(i, 1)
        """

if __name__ == '__main__':
    main()