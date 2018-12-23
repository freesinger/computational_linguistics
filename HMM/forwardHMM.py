import os
import numpy as np

traindir = '/Users/shanewang/Desktop/train/'
testdir = '/Users/shanewang/Desktop/test/'
validdir = '/Users/shanewang/Desktop/valid/'
resdir = '/Users/shanewang/Desktop/results/'

train_doc = os.listdir(path=traindir)
test_doc = os.listdir(path=testdir)
valid_doc = os.listdir(path=validdir)
tag = {}    # tag: frequency
pair_tag = {}   # (currenet_tag, previous_tag): frequency
word_tag_freq = {}  # (word, tag): frequency
word_tag = {}   # word: [tags]
test_proc_sentence = []    # store sentences in test without tag
valid_proc_sentence = []    # store sentences in valid without tag

def train_text_proc(text):
    with open(text, 'r', encoding='gbk') as t:
        s = t.readlines()
        for sentence in s:
            sentence = sentence.split()[1:-1]
            # tag = {}
            # word_tag_freq = {}
            for word in sentence:
                temp = word.split('/')
                if temp[1] not in tag:
                    tag[temp[1]] = 1
                else:
                    tag[temp[1]] += 1
                tup = (temp[0], temp[1])
                if tup not in word_tag_freq:
                    word_tag_freq[tup] = 1
                else:
                    word_tag_freq[tup] += 1
            # pair_tag = {}
            for i in range(1, len(sentence) - 3):
                pretag = sentence[i].split('/')[1]
                curtag = sentence[i + 1].split('/')[1]
                tup = (curtag, pretag)
                if tup not in pair_tag:
                    pair_tag[tup] = 1
                else:
                    pair_tag[tup] += 1
            # word-tag = {}
            for word in sentence:
                temp = word.split('/')
                if temp[0] not in word_tag:
                    word_tag[temp[0]] = [temp[1]]
                elif temp[1] not in word_tag[temp[0]]:
                    word_tag[temp[0]].append(temp[1])
            # proc_sentence = []
            for p in range(len(sentence)):
                sentence[p] = sentence[p].split('/')[0]

# proc_sentence = []
def text_proc(text, path):
    with open(text, 'r', encoding='gbk') as t:
        s = t.readlines()
        for sentence in s:
            sentence = sentence.split()[1:-1]
            """
            # change w won't change sentence[]
            for w in sentence:
                tmp = w.split('/')
                w = tmp[0]
            """
            for p in range(len(sentence)):
                sentence[p] = sentence[p].split('/')[0]
            path.append(sentence)
            
def freq_analysis(dic):
    total = 0
    for i in dic:
        total += dic[i]
    for i in dic:
        dic[i] /= total

def init(firstword):
    if word_tag.__contains__(firstword):
        tagset = word_tag[firstword]
    else:
        return 0
    curval = 0
    for t in tagset:
        curval += tag[t] * word_tag_freq[(firstword, t)]
    return curval

def HMMcalculate(preword, curword):
    curval = 0
    if word_tag.__contains__(preword):
        p_tagset = word_tag[preword]
    else:
        return 0
    if word_tag.__contains__(curword):
        curtagset = word_tag[curword]
    else:
        return 0
    for cur in curtagset:
        for pre in p_tagset:
            if not pair_tag.__contains__((cur, pre)):
                pair_tag.update({(cur, pre): 0})
            else:
                curval += pair_tag[(cur, pre)] * word_tag_freq[(curword, cur)]
    return curval

def forwardHMM(sentence):
    value = []
    for i in range(len(sentence) - 1):
        if i == 0:
            PI = init(sentence[0])
            value.append(PI)
        else:
            temp = HMMcalculate(sentence[i], sentence[i + 1])
            value.append(temp)
    return(np.prod(value))

def main():
    if not os.path.exists(resdir):
        os.makedirs(resdir)
    with open(resdir + 'result.txt', 'w', encoding='gbk') as res:
        for i in train_doc:
            if i == 'DS_Store':
                train_doc.remove(i)
        for file in train_doc:
            train_text_proc(traindir + file)
        freq_analysis(tag)
        freq_analysis(pair_tag)
        freq_analysis(word_tag_freq)
        for file in test_doc:
            text_proc(testdir + file, test_proc_sentence)
        for file in valid_doc:
            text_proc(validdir + file, valid_proc_sentence)
        print("Process Done!")

        for sentence in test_proc_sentence:
            res.write(str(forwardHMM(sentence)) + '| \t')
        res.write('\n')
        for sentence in valid_proc_sentence:
            res.write(str(forwardHMM(sentence)) + '| \t')
        print("Done!")
            
if __name__ == "__main__":
    main()