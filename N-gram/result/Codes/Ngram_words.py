import os
import pickle
import copy

rootdir = '/Users/shanewang/Desktop/nlp'
newdir = '/Users/shanewang/Desktop/preprc'
train_dir= '/Users/shanewang/Desktop/preprc/train'
test_dir= '/Users/shanewang/Desktop/preprc/test'
valid_dir= '/Users/shanewang/Desktop/preprc/valid'
result= '/Users/shanewang/Desktop/result'

total_words=0   #训练集中词个数
V=0             #不同词数
total_pairs=0   #词组数
V_pairs=0       #不同词组数
prob_unigram={}     #每个词得样本概率
prob_bigram={}     #每个词得样本概率

#预处理每行加起始符和结束符，以行为句
def Pretreatment(rootdir,newdir):
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in list:
        if i == '.DS_Store':
            list.remove('.DS_Store')
    #预处理每行加起始符和结束符
    for i in range(len(list)):
        path = os.path.join(rootdir,list[i])
        filelist=os.listdir(path)
        #print(filelist)
        for j in range(len(filelist)):
            filepath = os.path.join(path,filelist[j])
            if os.path.isfile(filepath):
                newfilepath=newdir+'/'+list[i]
                isExists=os.path.exists(newfilepath)
                if not isExists:
                    os.makedirs(newfilepath)
                newfilepath=newfilepath+'/'+filelist[j]
                with open(filepath, 'r+', encoding='gbk') as f,open(newfilepath, 'w', encoding='gbk') as f1:
                    for x in f:
                        f1.write('<BOS>  '+x[:len(x)-1]+'<EOS>  \n')

def AddnewGram(dict_words,wd):
    for w in wd:       
        if dict_words. __contains__(w):
            dict_words[w]+=1
        else:
            dict_words[w]=1    

def Addbigram(dict_words,wd):
    nxt_word={}
    length=len(wd)
    for i in range(length-1):       
        if dict_words. __contains__(wd[i]):
            if dict_words[wd[i]].__contains__(wd[i+1]):
                dict_words[wd[i]][wd[i+1]]+=1
            else:
                dict_words[wd[i]][wd[i+1]]=1
        else:
            nxt_word[wd[i+1]]=1
            dict_words[wd[i]]=nxt_word    

#将字典数据存为二进制文件，避免多次计算    
def save_obj(obj, name ):
    with open(newdir +'/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#读取之前的字典数据
def load_obj(name ):
    with open(newdir +'/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

#存储指定文件夹序列数据至指定处,unigram
def savefile2pkl(dirpath,name):
    #存储数据，字典
    word_times={}
    filelist = os.listdir(dirpath) #列出文件夹下所有的目录与文件
    for i in range(0,len(filelist)):
        filepath = os.path.join(dirpath,filelist[i])
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='gbk') as f:
                for x in f:
                    sentence=x.split("  ")
                    length=len(sentence)
                    AddnewGram(word_times,sentence[:length-1])
    save_obj(word_times,name)

#存储指定文件夹序列数据至指定处,bigram
def saveBigram2file(dirpath,name):
    dict_bi={}
    filelist = os.listdir(dirpath) #列出文件夹下所有的目录与文件
    for i in range(0,len(filelist)):
        filepath = os.path.join(dirpath,filelist[i])
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='gbk') as f:
                for x in f:
                    sentence=x.split("  ")
                    length=len(sentence)
                    Addbigram(dict_bi,sentence[:length-1])
    save_obj(dict_bi,name)

#计算总词数
def count_num_words(word_times):
    number=0
    items=word_times.items()
    for word,count in items:
        number+=count
    return number

#计算总bigram数,不同bigram数
def count_pairs_num(pair_times):
    number=0
    types=0
    items=pair_times.items()
    for word,nxt in items:
        types+=len(nxt)
        nxt_items=nxt.items()
        for nxt_word,count in nxt_items:
            number+=count
    return number,types

#计算词汇数
def count_num_types(word_times):
    return len(word_times)-1    #减去起始符

#add-one, unigram
def laplace_unigrams(word_times,total,V):
    prob_word=copy.deepcopy(word_times)
    items=word_times.items()
    for word,count in items:
        prob_word[word]=(count+1)/(total+V)
    return prob_word

#add-one, bigram
def laplace_bigrams(pair_times,word_times,total,V):
    prob_word=copy.deepcopy(pair_times)
    items=pair_times.items()
    for word,nxt in items:
        nxt_items=nxt.items()
        for nxt_word,count in nxt_items:
            prob_word[word][nxt_word]=(count+1)/(word_times[word]+V_pairs)
    return prob_word

#good-turing smoothing,unigram
def gt_unigram(word_times,c_times,total):
    prob_word=copy.deepcopy(word_times)
    items=word_times.items()
    for word,num in items:
        if c_times.__contains__(num+1):
            prob=(num+1)*c_times[num+1]/(c_times[num]*total)
        else:
            prob=num/total
        prob_word[word]=prob
    return prob_word

#good-turing smoothing,bigram
def gt_bigram(pair_times,c_times,total):
    prob_word=copy.deepcopy(pair_times)
    items=pair_times.items()
    for word,nxt in items:
        nxt_items=nxt.items()
        for nxt_word,num in nxt_items:
            if c_times.__contains__(num+1):
                prob=(num+1)*c_times[num+1]/(c_times[num]*total)
            else:
                prob=num/total
            prob_word[word][nxt_word]=prob
    return prob_word


#统计出现相同个数的词的个数
def count_same_times(word_times):
    c_times={}
    items=word_times.items()
    for word,count in items:
        if c_times.__contains__(count):
            c_times[count]+=1
        else:
            c_times[count]=1
    return c_times

#计算相同次的bigram数
def count_same_pairs(pair_times):
    c_times={}
    items=pair_times.items()
    for word,nxt in items:
        nxt_items=nxt.items()
        for nxt_word,count in nxt_items:
            if c_times.__contains__(count):
                c_times[count]+=1
            else:
                c_times[count]=1
    return c_times

#unigram,Laplace
def sentence_Perplexity(set_path,newfilename):
    filelist = os.listdir(set_path) #列出文件夹下所有的目录与文件
    newfilepath=os.path.join(result,newfilename)
    count=0
    for i in range(0,len(filelist)):
        filepath = os.path.join(set_path,filelist[i])
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='gbk') as f,open(newfilepath, 'a', encoding='gbk') as f1:
                for x in f:
                    sentence=x.split("  ")
                    length=len(sentence)-1
                    prob_s=1.0
                    for word in range(length):
                        if prob_unigram.__contains__(sentence[word]):
                            prob_s*=prob_unigram.get(sentence[word])
                        else:
                            prob_s*=1/(total_words+V)
                    if prob_s==0.0:
                        count+=1
                        f1.write('NULL\t')
                        continue
                    else:
                        pp=pow(prob_s,-(1/length))
                        pp='%.2f' % pp
                        f1.write(str(pp)+'\t')
    with open(newfilepath, 'a', encoding='gbk') as f1:
        f1.write('\n')
    print(count)

#bigram,Laplace
def sentence_bi_Perplexity(set_path,newfilename):
    filelist = os.listdir(set_path) #列出文件夹下所有的目录与文件
    newfilepath=os.path.join(result,newfilename)
    count=0
    for i in range(0,len(filelist)):
        filepath = os.path.join(set_path,filelist[i])
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='gbk') as f,open(newfilepath, 'a', encoding='gbk') as f1:
                for x in f:
                    sentence=x.split("  ")
                    length=len(sentence)-1
                    prob_s=1.0
                    for word in range(length-1):
                        if prob_bigram.__contains__(sentence[word]) and prob_bigram[sentence[word]].__contains__(sentence[word+1]):
                            prob_s*=prob_bigram[sentence[word]][sentence[word+1]]
                        else:
                            prob_s*=1/(total_pairs+V_pairs)
                    if prob_s==0.0:
                        count+=1
                        f1.write('NULL\t')
                        continue
                    else:
                        pp=pow(prob_s,-(1/length))
                        pp='%.2f' % pp
                        f1.write(str(pp)+'\t')
    with open(newfilepath, 'a', encoding='gbk') as f1:
        f1.write('\n')
    print(count)

#unigram,GT
def gt_sentence_Perplexity(set_path,newfilename,c_times):
    filelist = os.listdir(set_path) #列出文件夹下所有的目录与文件
    newfilepath=os.path.join(result,newfilename)
    count=0
    for i in range(0,len(filelist)):
        filepath = os.path.join(set_path,filelist[i])
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='gbk') as f,open(newfilepath, 'a', encoding='gbk') as f1:
                for x in f:
                    sentence=x.split("  ")
                    length=len(sentence)-1
                    prob_s=1.0
                    for word in range(length):
                        if prob_unigram.__contains__(sentence[word]):
                            prob_s*=prob_unigram.get(sentence[word])
                        else:
                            prob_s*=c_times[1]/(total_words)
                    if prob_s==0.0:
                        count+=1
                        f1.write('NULL\t')
                        continue
                    else:
                        pp=pow(prob_s,-(1/length))
                        pp='%.2f' % pp
                        f1.write(str(pp)+'\t')
    with open(newfilepath, 'a', encoding='gbk') as f1:
        f1.write('\n')
    print(count)

#bigram,GT
def gt_sentence_bi_Perplexity(set_path,newfilename,c_times):
    filelist = os.listdir(set_path) #列出文件夹下所有的目录与文件
    newfilepath=os.path.join(result,newfilename)
    count=0
    for i in range(0,len(filelist)):
        filepath = os.path.join(set_path,filelist[i])
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='gbk') as f,open(newfilepath, 'a', encoding='gbk') as f1:
                for x in f:
                    sentence=x.split("  ")
                    length=len(sentence)-1
                    prob_s=1.0
                    for word in range(length-1):
                        if prob_bigram.__contains__(sentence[word]) and prob_bigram[sentence[word]].__contains__(sentence[word+1]):
                            prob_s*=prob_bigram[sentence[word]][sentence[word+1]]
                        else:
                            prob_s*=c_times[1]/(total_pairs)
                    if prob_s==0.0:
                        count+=1
                        f1.write('NULL\t')
                        continue
                    else:
                        pp=pow(prob_s,-(1/length))
                        pp='%.2f' % pp
                        f1.write(str(pp)+'\t')
    with open(newfilepath, 'a', encoding='gbk') as f1:
        f1.write('\n')
    print(count)

if __name__ == '__main__':
    
    # 1.txt (unigram)
    Pretreatment(rootdir,newdir)
    #Pretreatment_punctuation(rootdir,newdir)
    #存储训练数据，字典，一次即可
    savefile2pkl(train_dir,"train_1.1")
    #加载训练集字典
    word_times=load_obj("train_1.1")
    #计算总词数
    total_words=count_num_words(word_times)
    #词汇数
    V=count_num_types(word_times)
    #获取每个词得概率，字典
    prob_unigram=laplace_unigrams(word_times,total_words,V)
    save_obj(prob_unigram,"prob_unigram")
    #prob_unigram=load_obj("prob_unigram")
    sentence_Perplexity(valid_dir,"validUni_1.txt")
    sentence_Perplexity(test_dir,"testUni_1.txt")
    
    # 1.txt (bigram)
    #存储训练数据，字典，bigram,一次即可
    saveBigram2file(train_dir,"train_bi")
    #加载训练集字典
    pair_times=load_obj("train_bi")
    word_times=load_obj("train_1.1")
    #计算总bigram数,不同bigram个数
    total_pairs,V_pairs=count_pairs_num(pair_times)
    #获取每个词得概率，字典
    prob_bigram=laplace_bigrams(pair_times,word_times,total_pairs,V_pairs)
    save_obj(prob_bigram,"prob_bigram")
    #prob_bigram=load_obj("prob_bigram")
    
    sentence_bi_Perplexity(valid_dir,"validBin_1.txt")
    sentence_bi_Perplexity(test_dir,"testBin_1.txt")
    
    # 2.txt (unigram)
    c_times=count_same_times(word_times)
    #计算总词数
    total_words=count_num_words(word_times)
    #获取每个词得概率，字典
    prob_unigram=gt_unigram(word_times,c_times,total_words)
    save_obj(prob_unigram,"prob_unigram_gt")
    #prob_unigram_gt=load_obj("prob_unigram_gt")
    gt_sentence_Perplexity(valid_dir,"validUni_2.txt",c_times)
    gt_sentence_Perplexity(test_dir,"testUni_2.txt",c_times)
    
    # 2.txt (bigram)
    pair_times=load_obj("train_bi")

    c_times=count_same_pairs(pair_times)
    total_pairs,t=count_pairs_num(pair_times)
    prob_bigram=gt_bigram(pair_times,c_times,total_pairs)
    save_obj(prob_bigram,"prob_bigram_gt")
    #prob_bigram_gt=load_obj("prob_bigram_gt")
    gt_sentence_bi_Perplexity(valid_dir,"validBig_2.txt",c_times)
    gt_sentence_bi_Perplexity(test_dir,"testBig_2.txt",c_times)
