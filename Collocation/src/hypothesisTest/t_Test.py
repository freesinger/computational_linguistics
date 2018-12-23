import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store result of frequences
dict_res = {}
word_cnt = {}
doc = list(os.listdir(rootdir))  

def text_process(text):
    single_npair = []
    with open(text, 'r', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            proc_sentence = []
            for word in sentence:
                temp = word.split('/')
                if temp[1] != 'w':
                    word = temp[0]
                    word_fre_analysis(word)
                    proc_sentence.append(word)          
            for pos in range(len(proc_sentence) - 1):
                single_npair.append((proc_sentence[pos], proc_sentence[pos + 1]))
    return single_npair

def pair_fre_analysis(textpair):
    # nodup_pair =[]
    for pair in textpair:
        if not dict_res.__contains__(pair):
            dict_res[pair] = 1
            # dict_res.update({pair : 1})
        else:
            dict_res[pair] += 1

def word_fre_analysis(curword):
    # global word_cnt
    if not word_cnt.__contains__(curword):
        word_cnt[curword] = 1
    else:
        word_cnt[curword] += 1
        
def word_fre_compute(curword, totalbigram):
    return word_cnt[curword] / totalbigram

def t_Test(curpair, t):
    # print(type(curpair))
    # cur = ' '.join(str(i) for i in curpair)
    # words = cur.split()
    """
    print(pow(dict_res[curpair] / pow(t, 2), 1/2))
    print(curpair,dict_res[curpair],words[0], word_cnt[words[0]],words[1], word_cnt[words[1]])
    print((dict_res[curpair] / t), word_fre_compute(words[0], t), word_fre_compute(words[1], t))
    print(pow(dict_res[curpair] / pow(t, 2), 1/2))
    print((dict_res[curpair] / t) - word_fre_compute(words[0], t) * word_fre_compute(words[1], t))
    """
    t_result = ((dict_res[curpair] / t) - word_fre_compute(curpair[0], t) * word_fre_compute(curpair[1], t)) \
        / pow(dict_res[curpair] / pow(t, 2), 1/2)
    # print(t_result)
    return t_result

def sort_result(result):
    sorted_res = sorted(dict_res.items(), key = lambda k: k[1])
    # res.append([pair, num] for pair, num in dict_res())
    for i in reversed(sorted_res):
        if i[1] > 5:
            result.write(' '.join(str(s) for s in i) + '\n')

def main():
    with open(resdir + '3_a.txt', 'w', encoding='gbk') as res:
        testres = []
        for i in doc:
            if i == '.DS_Store':
                doc.remove(i)
        print("Total", len(doc), "texts")
        for i in range(len(doc)):
            cur_pair = text_process(rootdir + doc[i])
            pair_fre_analysis(cur_pair)
        print("Preprocess done!")
        total_bigram = sum(dict_res.values())

        sort_res = []
        tmp_res = reversed(sorted(dict_res.items(), key = lambda k : k[1]))
        for i in tmp_res:
            if i[1] > 3: 
                sort_res.append(i)
        for i in sort_res:
            # print(i, i[0])
            t_res = t_Test(i[0], total_bigram)
            # print(t_res)
            testres.append((i, t_res))
        for i in testres:
            res.write(' '.join(str(t) for t in i) + '\n')
            
        print("Done!")
        
if __name__ == '__main__':
    main()