import os

tempdir = '/Users/shanewang/Desktop/result/tempRes'
#validBig = '~/Desktop/result/valid_big.txt'
#testUni = '~/Desktop/result/test_uni.txt'
#testBig = '~/Desktop/result/test_big.txt'



def anaysis(dir):
    folder_list = os.listdir(tempdir)
    for i in folder_list:
        if i == '.DS_Store':
            folder_list.remove('.DS_Store')
    
    for i in range(len(folder_list)):
        text = os.path.join(tempdir, folder_list[i])
        res = 0.0
        with open(text, 'r', encoding = 'gbk') as f:
            for line in f:
                x = line.split('\t')
                # x.remove('\n')
                len_x = len(x)
                for cha in x:
                    if cha == 'NULL' or cha == '\n':
                        len_x -= 1
                        continue
                       
                    res += float(cha)
        res /= len_x
        # format(res, '.2f')
        print(folder_list[i])
        print(res)

if __name__ == '__main__':
    anaysis(tempdir)
            