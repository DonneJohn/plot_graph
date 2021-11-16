#!/usr/bin/python3
import os
import re
import numpy as np



#filename = "2020_10_16_14_0.log"
#print("文件名：", filename)


'''
正则过滤log文件，查找所有的时间点的重量数据，以键值对的方式返回
'''
def Find(string):
    #data = re.findall('(?P<t>\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) D/STATE: onWeightStateRecieve\s(?P<weight>\d+\.\d+)', string)
    data = re.findall('(?P<t>\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\s+E/AHS:\s+STATEcom.aihuishou.fenlei.common.ui.removal.RemovalActivity\s+onWeightStateRecieve\s+(?P<weight>\d+\.\d+)', string)
    #data = re.findall('(?P<t>\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\s+E/AHS:\s+STATEcom.aihuishou.fenlei.common.ui.press.PressNewLoginActivity\s+onWeightStateRecieve\s+(?P<weight>\d+\.\d+)', string)
    return data



def getLogfileData(logfilename):
    with open(logfilename) as f:
        str = f.read()
        # print("get data:", Find(str))
        return Find(str)

def getdata(orderfilename):
    dirpath = os.getcwd()
    print("当前目录：", dirpath)
    filePath = dirpath + "/" + orderfilename
    with open(filePath, 'r', encoding='UTF-8') as f:
        str = f.read()
        # print("get data:", Find(str))
        return Find(str)

'''
算术平均滤波法
'''
def ArithmeticAverage(inputs, per):
    if np.shape(inputs)[0] % per != 0:
        lengh = np.shape(inputs)[0] / per
        for x in range(int(np.shape(inputs)[0]),int(lengh + 1)*per):
            inputs = np.append(inputs,inputs[np.shape(inputs)[0]-1])
    inputs = inputs.reshape((-1,per))
    mean = []
    for tmp in inputs:
        mean.append(tmp.mean())
    return mean

'''
滑动平均滤波算法
'''
def filter(datas, per):
    size = len(datas)
    print("length:", size)
    
    weights = [i[1] for i in datas]
    preweights = weights[slice(0, per)]
    print("preweights:", preweights)

    newdatas = [] * size
    newdatas[0:per] = preweights
    print("newdatas pre:", newdatas)

    value_buff = [] * per
    value_buff = preweights
    for data in weights[per:]:
        value_buff.pop(0)
        value_buff.append(data)
        newdata = np.mean(list(map(float, value_buff)))
        # print("新数据：", newdata)
        newdatas.append(newdata)

    for i in range(len(newdatas)):
        #"{:.1f}".format(data)
        newdatas[i] = round(float(newdatas[i]),1)
        #print("data:",data)
    #print("新数据：", newdatas)
    return list(zip([i[0] for i in datas],newdatas))


'''
查找拖筐后和放筐前的时间节点
连续下降点1
连续上升点2
不变的点0
'''
def findCleanPoints(datas):
    signs = ""
    size = len(datas)
    timePoints = [i[0] for i in datas]
    weights = [i[1] for i in datas]
    for i in range(size):
        if i < size-1:
            diff = weights[i] - weights[i+1]
            if diff > 0:
                signs += "1"
            elif diff <0:
                signs += "2"
            else:
                signs +="0"
    #print("signs:", signs)
    downSigns = dealRepeatData(signs, "1")
    print("downSignsDict:", downSigns)
    print("连续下降曲线的时间点", downSigns.keys())
    upSigns = dealRepeatData(signs, "2")
    print("downSignsDict:", upSigns)


    #下降点取第一条下降点线段，然后取最后一个点作为拖筐后的点

    #优化，先从数据中找出重量最低的点，再找最靠近最低点的下降点坐标
    minWeight = min(weights)
    minIndex = weights.index(minWeight)
    print("最低点重量：", minWeight)
    print("最低点的第一个下标：", minIndex)

    if downSigns is not None:
        pullBasketIndex = min(downSigns.keys(), key=lambda x: abs(x[1]-minIndex))[1]
        # downLastIndexList = [for i in downSigns.keys[1] for y =abs(i - minIndex)]
        print("pullBasketIndex:", pullBasketIndex)

       
    print("拖筐出来的时间点为：", timePoints[pullBasketIndex])
    print("拖筐出来的时间点重量为：", weights[pullBasketIndex])



    #上升点，取靠近清运完成的重量的一条上升曲线，以及连续时间最长的一条上升曲线，两条曲线如果是同一条则取取一条，不同则取两条
    #stableSigns = dealRepeatData(signs, "0")
    #len(signs) - signs[::-1].index(stableSigns[::-1]) - len(maxUpSign)
    if upSigns is not None:
        pushBasketIndex = max(upSigns.keys(), key=lambda x: abs(x[1]-x[0]))[0]
        print("pushBasketIndex:", pushBasketIndex)

    print("放筐进去的时间点为：", timePoints[pushBasketIndex])
    print("放筐进去的时间点重量为：", weights[pushBasketIndex])
    return [(timePoints[pullBasketIndex], weights[pullBasketIndex]), (timePoints[pushBasketIndex], weights[pushBasketIndex])]

def unique_index(L,e):
    return [j for (i,j) in enumerate(L) if i == e]    

def dealRepeatData(signs, value):
    # filterStr = "(" + value + ")" + "{3,}"
    filterStr = value + "{3,}"
    pattern = re.compile(filterStr)
    # print("pattern:", pattern)
    it = re.finditer(pattern, signs)
    filterSignsDict = {}
    for match in it:
        print("match group:", match.group())
        print("match index:", match.span())
        filterSignsDict[match.span()] = match.group()

    print("filterSignsDict:", filterSignsDict)
    '''
    filterSigns = re.findall(pattern, signs)
    if filterSigns is None or len(filterSigns) == 0:
          return None

    return filterSigns
    '''
    if filterSignsDict is None or len(filterSignsDict) ==0:
        return None
    return filterSignsDict

def getlogs():
    dirpath = os.getcwd()
    print("当前目录：", dirpath)
    fileDir = dirpath + "/log" 
    files = os.listdir(fileDir)
    files = [fileDir + "/" + f for f in files if f.endswith('.log')]
    print("当前目录 logs：", files)
    return files
# datas = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11)]
# print("过滤后的数据", filter(datas, 5))