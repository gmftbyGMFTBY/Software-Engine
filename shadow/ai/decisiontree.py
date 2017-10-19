#!/usr/bin/python3

import sys
sys.path.append('..')
import sql.sql as sql    # 导入数据库存储模块
from math import log
import operator
import pprint

def load_data():
    '''
    该函数从数据库中抽取所有的样本空间数据，将信息规整病返还给监督学习组件去学习
    '''
    save = sql.main(5)    # 获取全部的样本信息
    # data
    data = []
    for i in save:
        p = i[1:4] + i[5:] + (i[4],)
        data.append(list(p))
    label = ['content size' , 'number_reader' , 'number_like' , 'number_code' , 'number_photo' , 'number_link']
    return data , label

def calShannoneEnt(dataset):
    '''
    该函数计算香农熵
    '''
    length = len(dataset)
    label = {}
    for i in dataset:
        currentlabel = i[-1]
        if currentlabel not in label.keys():
            label[currentlabel] = 0
        label[currentlabel] += 1
    shannonEnt = 0.0
    for key in label:
        p = float(label[key]) / length
        shannonEnt -= p * log(p , 2)
    return shannonEnt

def splitdataset(dataset , axis , value):
    '''
    该函数用来根据 data[axis] = value 划分数据集
    '''
    ret = []
    for i in dataset:
        if i[axis] == value:
            p = i[:axis]
            p.extend(i[axis + 1 :])
            ret.append(p)
    return ret

def choosebestfeaturetosplit(dataset):
    '''
    该函数遍历所有的特征，试图在本次的询问中找到最合适的特征进行分支的划分
    '''
    numfeature = len(dataset[0]) - 1
    # 初始化基础的信息熵，信息增益和最优的选择
    baseentroy = calShannoneEnt(dataset)
    baseinfogain = 0.0
    bestfeature = -1
    for i in range(numfeature):
        fealist = [example[i] for example in dataset]
        uniquevals = set(fealist)    # 找到dataset数据集在i特征上的值分布
        newentroy = 0
        for value in uniquevals:
            subdataset = splitdataset(dataset , i , value)    # 分支i的子集
            p = len(subdataset) / float(len(dataset))    # 分支i的总量概率
            newentroy += p * calShannoneEnt(subdataset)    # 概率信息增益
        infogain = baseentroy - newentroy    # 只要infogain越大代表选择越好
        if infogain > baseinfogain :
            baseinfogain = infogain
            bestfeature = i
    return bestfeature

def major(data):
    '''
    当组内的标签用完了还是没有完全的划分好我们的子集样本的时候，我们需要多数选择机制(标签)
    '''
    classcount = {}
    for i in data:
        if i not in classcount.keys():
            classcount[i] = 0
        classcount[i] += 1
    save = sorted(classcount.iteritems() , key = operator.itemgetter(1) , reverse = True)
    return save[0][0]

def createtree(dataset , label):
    '''
    该函数递归构建 ID3 决策树
    '''
    classlist = [example[-1] for example in dataset]    # 子集的标签列表
    if classlist.count(classlist[0]) == len(classlist):
        # 子集样本同一特征
        return classlist[0]
    if len(dataset[0]) == 1:
        # 子集没有可供筛选询问的特征,多数返回
        return major(classlist)
    bestfeature = choosebestfeaturetosplit(dataset)    # 按照香农熵计算信息增益选择最合适的分类特征
    bestfeaturelabel = label[bestfeature]    # 获取特征的名称
    tree = {bestfeaturelabel : {}}    # 构建树
    del label[bestfeature]
    featurevalues = [example[bestfeature] for example in dataset]
    uniquevalue = set(featurevalues)    # 该最好特征值域别
    for value in uniquevalue:
        sublabel = label[:]
        tree[bestfeaturelabel][value] = createtree(splitdataset(dataset , bestfeature , value) , sublabel)
    return tree

def save_model_to_sql(user , model):
    '''
    该函数将产生的字典型决策树模型存储在数据库的user表中
    '''
    model = str(model)
    save = sql.main(8 , **{'old_name' : user , 'model' : model})
    print(save)

def get_model_from_sql(user):
    '''
    该函数将存储在数据库中的决策树模型提取出来
    '''
    save = sql.main(1 , **{'name' : user})
    tree = eval(save[3])
    return tree

if __name__ == "__main__":
    '''
    dataset , label = load_data()
    mytree = createtree(dataset , label)
    save_model_to_sql('xuhengda' , mytree)
    new_tree = get_model_from_sql('xuhengda')
    '''
    pass
