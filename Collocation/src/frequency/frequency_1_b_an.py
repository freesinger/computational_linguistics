import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store result of frequences
dict_res = {}

def text_process(text):
    single_npair = []
    with open(text, 'r', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            # print(sentence[0][-1])
            for pos in range(len(sentence) - 1):
                if sentence[pos][-2:] == '/a' and sentence[pos + 1][-2:] == '/n':
                    single_npair.append((sentence[pos][:-2], sentence[pos + 1][:-2]))
            # print(single_npair)
    return single_npair

def fre_analysis(textpair):
    # nodup_pair =[]
    for pair in textpair:
        if not dict_res.__contains__(pair):
            dict_res.update({pair : 1})
            # dict_res[pair] = 1
        else:
            dict_res[pair] += 1

def sort_result(result):
    sorted_res = sorted(dict_res.items(), key = lambda k: k[1])
    # res.append([pair, num] for pair, num in dict_res())
    for i in reversed(sorted_res):
        if i[1] > 0:
            result.write(' '.join(str(s) for s in i) + '\n')

def main():
    if not os.path.exists(resdir):
        os.mkdir(resdir)
    with open(resdir + '1_b_an.txt', 'w', encoding='gbk') as res:
        doc = list(os.listdir(rootdir))       
        for i in doc:
            if i == '.DS_Store':
                doc.remove(i)
        print(len(doc))
        for i in range(len(doc)):
            cur_pair = text_process(rootdir + doc[i])
            fre_analysis(cur_pair)
        print("Preprocess done!")
        sort_result(res)
        print("Done!")
        
if __name__ == '__main__':
    main()