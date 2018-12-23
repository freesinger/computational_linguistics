import os

rootdir = '/Users/shanewang/Desktop/test/'
resdir = '/Users/shanewang/Desktop/'
neb_pair = []

def text_process(text):
    with open(text, 'r', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            proc_sentence = []
            for word in sentence:
                temp = word.split('/')
                if temp[1] != 'w':
                    word = temp[0]
                    proc_sentence.append(word)
            
            for pos in range(len(proc_sentence) - 1):
                neb_pair.append((proc_sentence[pos], proc_sentence[pos + 1]))

def fre_analysis( result):
    res = []
    nodup_pair =[]
    for pair in neb_pair:
        if pair not in nodup_pair:
            nodup_pair.append(pair)
    dict_res = {pair : 0 for pair in nodup_pair}

    for pair in neb_pair:
        if pair in dict_res:
            dict_res[pair] += 1

    sorted_res = sorted(dict_res.items(), key = lambda k: k[1])
    # res.append([pair, num] for pair, num in dict_res())
    for i in reversed(sorted_res):
        if i[1] > 10:
            result.write(' '.join(str(s) for s in i) + '\n')

def main():
    with open(resdir + 'result.txt', 'w', encoding='gbk') as res:
        doc = list(os.listdir(rootdir))
        for i in doc:
            if i == '.DS_Store':
                doc.remove(i)
        print(len(doc))
        for i in range(len(doc)):
            text_process(rootdir + doc[i])
        print("Preprocess done!")
        fre_analysis(res)
        print("Done!")
        
if __name__ == '__main__':
    main()