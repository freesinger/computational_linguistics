with open('/Users/shanewang/Desktop/train/01240704.txt', 'r', encoding='gbk') as f:
    for sentence in f:
        # sentence.rstrip('\n')
        sentence = sentence.split()
        proc_sentence = []
        for word in sentence:
            temp = word.split('/')
            if temp[1] != 'w':
                word = temp[0]
                proc_sentence.append(word)
        neib_pair = []
        for pos in range(len(proc_sentence) - 1):
            #if proc_sentence[pos + 1] != '\n':
                #print([proc_sentence[pos], proc_sentence[pos + 1]])
            neib_pair.append([proc_sentence[pos], proc_sentence[pos + 1]])
    
        res = []
        nodup_res =[]
        for pair in neib_pair:
            cnt = 0
            for i in range(len(neib_pair)):
                if pair == neib_pair[i][0:2]:
                    cnt += 1
            pair.append(cnt)
            res.append(pair)
        
        for i in res:
            if i not in nodup_res:
                nodup_res.append(i)

        for i in nodup_res:
            if i[-1] > 1:
                print(i)