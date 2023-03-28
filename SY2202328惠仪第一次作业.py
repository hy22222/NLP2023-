import os
import re
import jieba
import math

#读取文件夹中的所有文件
path = 'data'
files = os.listdir(path)
text = []
for file in files:
    position = path+'\\'+file
    with open(position,'r',encoding='ANSI') as f:
        data = f.read()
        text.append(data)

#读stopwords
f = open('cn_stopwords.txt','r',encoding='utf-8')
stopwords = f.read().splitlines()
xx = '本书来自www.cr173.com免费txt小说下载站'
xx2 = '更多更新免费电子书请关注www.cr173.com'
# 去除符号及中文无意义stopwords
def filter(text):
    a = re.sub(xx, '', text)
    b = re.sub(xx2, '', a)
    pattern = '|'.join(stopwords)
    c = re.sub(pattern, '', b)
    d = re.sub(r'\*', '', c)
    e = re.sub(r'\.', '',d)
    f = re.sub(r'\n', '', e)
    g = re.sub(r'\u3000', '', f)
    return g

# 全文
alltext =''
for txt in text:
    s = filter(txt)
    alltext += ''.join(s)
#一个文本
# ss = {}
# alltext=''
# for i in range(len(text)):
#     ss[i] =text[i]
#     s = filter(ss[i])
#     alltext = ''.join(s)

#处理文本，不同的分词方式
#以单个字为单位处理
# word = [word for word in alltext]
#jieba分词，以词语为单位处理
word = jieba.lcut(alltext)

#一元模型
def cal_uni_entropy(word):
    # 统计出现的次数
    count_uni = {}
    for i in range(len(word)):
        count_uni[word[i]] = count_uni.get(word[i],0)+1
    word_num = sum(count_uni.values())
    un_entropy = 0

    for i in count_uni.keys():
        prob = count_uni[i]/word_num
        un_entropy -= prob*math.log(prob,2)
    print("一元模型的中文信息熵为：{:.2f}".format(un_entropy))
    return count_uni,un_entropy
count_uni,un_entropy = cal_uni_entropy(word)

#二元模型
def bi_entropy(word,count_uni):
    #数量
    count_bi = {}
    for i in range(len(word) - 1):
        count_bi[word[i], word[i + 1]] = count_bi.get((word[i], word[i + 1]), 0) + 1
    b_entropy = 0
    word_num = sum(count_bi.values())
    for i in count_bi.keys():
        prob = count_bi[i]/word_num
        con_prob = count_bi[i]/count_uni[i[0]]
        b_entropy -= prob*math.log(con_prob,2)
    print("二元模型的中文信息熵为：{:.2f}".format(b_entropy))
    return count_bi,b_entropy
count_bi,bi_entropy = bi_entropy(word,count_uni)

#三元模型
def tri_entropy(word,count_bi):
    #数量
    count_tri = {}
    for i in range(len(word) - 2):
        count_tri[word[i], word[i + 1],word[i+2]] = count_tri.get((word[i], word[i + 1],word[i+2]), 0) + 1
    tr_entropy = 0
    word_num = sum(count_tri.values())
    for i in count_tri.keys():
        prob = count_tri[i]/word_num
        con_prob = count_tri[i]/count_bi[(i[0]),(i[1])]
        tr_entropy -= prob*math.log(con_prob,2)
    print("三元模型的中文信息熵为：{:.2f}".format(tr_entropy))
    return count_tri,tr_entropy
count_tri,tri_entropy = tri_entropy(word,count_bi)

