import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store result of frequences
dict_res = {}
pre_res = {}
aft_res = {}
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
                    # word_fre_analysis(word)
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

def pre_fre_analysis(textpair):
    for pair in textpair:
        if not pre_res.__contains__(pair[0]):
            pre_res[pair[0]] = 1
        else:
            pre_res[pair[0]] += 1

def aft_fre_analysis(textpair):
    for pair in textpair:
        if not aft_res.__contains__(pair[1]):
            aft_res[pair[1]] = 1
        else:
            aft_res[pair[1]] += 1

def find_O1O2(curtext):
    # O1 = curtext[0]
    O2 = curtext[1]
    return aft_res[O2] - dict_res[curtext]

def find_O2O1(curtext):
    O1 = curtext[0]
    # O2 = curtext[1]
    return pre_res[O1] - dict_res[curtext]

def X_square(curtext, t):
    w1w1 = dict_res[curtext]
    w1w2 = find_O1O2(curtext)
    w2w1 = find_O2O1(curtext)
    w2w2 = t - w1w1 - w1w2 - w2w1
    x_res = t * pow(w1w1 * w2w2 - w1w2 * w2w1, 2) / ((w1w1 + w1w2) * (w1w1 + w2w1) * (w1w2 + w2w2) * (w2w1 + w2w2))
    return x_res

def main():
    with open(resdir + '3_b.txt', 'w', encoding='gbk') as res:
        testres = []
        for i in doc:
            if i == '.DS_Store':
                doc.remove(i)
        print("Total", len(doc), "texts")
        for i in range(len(doc)):
            cur_pair = text_process(rootdir + doc[i])
            pair_fre_analysis(cur_pair)
            pre_fre_analysis(cur_pair)
            aft_fre_analysis(cur_pair)
        print("Preprocess done!")
        total_bigram = sum(dict_res.values())

        sort_res = []
        tmp_res = reversed(sorted(dict_res.items(), key = lambda k : k[1]))
        for i in tmp_res:
            if i[1] > 3: 
                sort_res.append(i)
        for i in sort_res:
            # print(i, i[0])
            X_res = X_square(i[0], total_bigram)
            # print(X_res)
            testres.append((i, X_res))
        for i in testres:
            res.write(' '.join(str(t) for t in i) + '\n')
            
        print("Done!")
        
if __name__ == '__main__':
    main()