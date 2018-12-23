import os

rootdir = '/Users/shanewang/Desktop/train/'
resdir = '/Users/shanewang/Desktop/results/'
# store result of frequences
dict_res = {}

# 改革/v  开放/v 
# 改革/vn 开放/vn
def text_process(text, dist):
    single_npair = []
    with open(text, 'r', encoding='gbk') as f:
        for sentence in f:
            sentence = sentence.split()
            # print(sentence[0][-1])
            if dist >= 0:           
                for pos in range(len(sentence) - 1):
                    if pos + dist < len(sentence) and sentence[pos][0:2] == '改革' \
                        and sentence[pos + dist][0:2] == '开放':
                        single_npair.append((sentence[pos][0:2], sentence[pos + dist][0:2], dist))
            else:
                for pos in range(len(sentence) - 1)[::-1]:
                    if pos + dist >= 0 and sentence[pos][0:2] == '改革' \
                        and sentence[pos + dist][0:2] == '开放':
                        single_npair.append((sentence[pos][0:2], sentence[pos + dist][0:2], dist))
            """
            for pos in range(len(sentence) - 1):
                if sentence[pos][-5:-3] == '改革' and sentence[pos + dist][-5:-3] == '开放':
                    single_npair.append((sentence[pos][:-3], sentence[pos + dist][:-3], dist))
            """
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
    with open(resdir + '2_b.txt', 'w', encoding='gbk') as res:
        doc = list(os.listdir(rootdir))       
        for i in doc:
            if i == '.DS_Store':
                doc.remove(i)
        print(len(doc))
        for step in range(-5, 6):
            for i in range(len(doc)):
                cur_pair = text_process(rootdir + doc[i], step)
                fre_analysis(cur_pair)
        print("Preprocess done!")
        sort_result(res)
        print("Done!")
        
if __name__ == '__main__':
    main()