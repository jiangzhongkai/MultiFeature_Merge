"""-*- coding: utf-8 -*-
 DateTime   : 2018/11/7 21:15
 Author  : Peter_Bonnie
 FileName    : util.py
 Software: PyCharm
"""

"""
辅助函数工具文件
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def reformat(samples,labels):
    """
    对标签进行one-hot编码
    :param samples:
    :param labels:
    :return:
    """
    samples=np.transpose(samples,(3,0,1,2))
    labels=np.array([x[0] for x in labels])
    one_hot_lables=[]
    for num in labels:
         one_hot=[0.0]*10 #生成10个0.0
         if num==10:
             one_hot[0]=1.0
         else:
             one_hot[num]=1.0
         one_hot_lables.append(one_hot)
    return samples,np.array(one_hot_lables).astype(np.float32)

# 计算accuracy
def getAccuracy(true, predictions):
	correct = 0
	for i in range(len(true)):
		if true[i] == predictions[i]:
			correct += 1
	accuracy = correct / float(len(true)) * 100.0
	return accuracy


# 计算精度（precision）
# 精度是精确性的度量，表示被分为正例的示例中实际为正例的比例
def getPrecision(testset, predictions):
	true_positives = 0
	sums = 0
	for i in range(len(testset)):
		if predictions[i] == 1:
			sums += 1
			if testset[i] == predictions[i]:
				true_positives = true_positives + 1
	if sums == 0:
		return 0
	precision = true_positives / float(sums) * 100.0
	return precision


# 计算召回率（recall）
# 召回率是覆盖面的度量，度量有多个正例被分为正例
def getRecall(testset, predictions):
	true_positives = 0
	sums = 0
	for i in range(len(testset)):
		if testset[i] == 1:
			sums += 1
		if predictions[i] == 1 and testset[i] == predictions[i]:
			true_positives = true_positives + 1
	recall = true_positives / float(sums) * 100.0
	return recall


def getF1(precision, recall):
	if (precision + recall) == 0:
		return 0
	else:
		F1 = (2*precision*recall)/(precision + recall)
		return F1





