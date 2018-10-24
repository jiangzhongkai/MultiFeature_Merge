"""-*- coding: utf-8 -*-
 DateTime   : 2018/10/24 16:20
 Author  : Peter_Bonnie
 FileName    : Plot_Fig.py
 Software: PyCharm
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Figure(object):
    """
    画图的类
    """
    def __int__(self):
        """
        初始化函数
        :return:
        """

    @staticmethod
    def plot_figure(data,save_name):
        """
        :param data:
        :return:
        """
        data = pd.read_csv(data)
        values = data.values[:1000]
        size=len(data.columns)
        group=[i for i in range(1,size,1)]
        i = 1
        plt.figure()
        for g in group:
            plt.subplot(len(group), 1, i)
            plt.plot(values[:,g])
            plt.xlabel("Date")
            plt.title(data.columns[g], y=0.5, loc="right")
            i += 1
        plt.savefig(save_name)
        plt.show()

        print("save fig successfully.")


if __name__=="__main__":
      pass




