"""-*- coding: utf-8 -*-
 DateTime   : 2018/9/2 16:03
 Author  : Peter_Bonnie
 FileName    : Beijing_LSTM
 Software: PyCharm
"""
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

"""
"""
class Data_Processing():
    """
    数据处理类
    """
    def __init__(self):
        pass

    #数据的预处理
    @staticmethod
    def parse(x):
        return datetime.strptime(x,'%Y %m %d %H')

    def count_0_num(self,data,pop_feat):
        """
        计算csv文件中除了时间以外所有特征全为0的数量
        :param data:
        :param pop_feat
        :return:
        """
        if isinstance(data,list):
            count={}
        else:
            count=0

        bool = False
        if not isinstance(data,list):
            tem_data = pd.read_csv(data)
            tem_data.pop(pop_feat)
            for i in range(tem_data.shape[0]):
                for col in tem_data.columns:
                    if tem_data.iloc[i][col] == 0:
                        bool = True
                    else:
                        bool = False
                        break
                if bool is True:
                    count += 1
        else:
            #获得每个数据集里面的为0的个数
            for path in data:
                temp_path=path.split('.')[0]
                tem_data=pd.read_csv(path)
                count[temp_path]=0
                tem_data.pop(pop_feat)
                for i in range(tem_data.shape[0]):
                    for col in tem_data.columns:
                        if tem_data.iloc[i][col]==0:
                            bool=True
                        else:
                            bool=False
                            break
                    if bool is True:
                        count[temp_path]+=1
        return count

    def fill_anomaly_data(self,data):
        """
        对异常值进行处理并填充
        :param data:
        :return:
        """

    def save_data_by_time(self,data):
        """
         把一个csv文件按照时间来划分
        主要是早上，07:00-09:00
        上午：09:00-12:00
        下午，12:00-19:00
        晚上:19:00-06:00
        :param data:
        :return:
        """
        data = pd.read_csv(data)
        # 早上
        morning_dataset = data[(data['measureTime'].map(lambda x: x.split(' ')[1]) >= '07:00:00')
                               & (data['measureTime'].map(lambda x: x.split(' ')[1]) <= '09:00:00')]
        # 上午
        shangwu_dataset = data[(data['measureTime'].map(lambda x: x.split(' ')[1]) >= '09:00:00')
                               & (data['measureTime'].map(lambda x: x.split(' ')[1]) <= '12:00:00')]
        # 下午
        afternoon_dataset = data[(data['measureTime'].map(lambda x: x.split(' ')[1]) >= '12:00:00')
                                 & (data['measureTime'].map(lambda x: x.split(' ')[1]) <= '19:00:00')]
        # 晚上
        evening_dataset_1 = data[(data['measureTime'].map(lambda x: x.split(' ')[1]) >= '19:00:00')
                                 & (data['measureTime'].map(lambda x: x.split(' ')[1]) <= '23:59:59')]

        evening_dataset_2 = data[(data['measureTime'].map(lambda x: x.split(' ')[1]) >= '00:00:00')
                                 & (data['measureTime'].map(lambda x: x.split(' ')[1]) <= '06:00:00')]

        evening_dataset = np.concatenate([evening_dataset_1, evening_dataset_2], axis=0)

        # 去掉值全为0的数据

        # 对异常值进行处理
        morning_dataset.to_csv("morning.csv", index=False)
        shangwu_dataset.to_csv("shangwu.csv", index=False)
        afternoon_dataset.to_csv("afternoon.csv", index=False)
        evening_dataset_1.to_csv("evening_1.csv", index=False)
        evening_dataset_2.to_csv("evening_2.csv", index=False)

        return morning_dataset, shangwu_dataset, afternoon_dataset, evening_dataset

    def load_dataset(self,data):
        """
        加载数据集
        :param data:
        :return:
        """
        dataset = pd.read_csv(data, header=0, index_col=0)
        columns = dataset.columns
        values = dataset.values
        # integer encode direction
        encoder = LabelEncoder()  # 标准化标签,将标签格式转换为range()范围内的数
        values[:, 4] = encoder.fit_transform(values[:, 4])
        # ensure all data is float
        values = values.astype('float32')
        # normalize features
        # scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = max_Min(values)
        # scaled = scaler.fit_transform(values)
        # frame as supervised learning
        reframed = series_to_supervised(scaled, 1, 1)
        # drop columns we don't want to predict
        reframed.drop(reframed.columns[[i for i in range(len(columns))]], axis=1, inplace=True)
        # print(reframed)
        return reframed

    def split_dataset_multiFeature(self,data, ratio=0.7):
        """
        分割数据集
        :param data:
        :return:
        """
        reframed = load_dataset(data)
        values = reframed.values

        len_size = int(reframed.shape[0] * ratio)
        train = values[:len_size, :]
        test = values[len_size:, :]

        # 用最后一列作为目标变量来预测
        train_x, train_y = train[:, :-1], train[:, -1]
        test_x, test_y = test[:, :-1], test[:, -1]

        # 变成网络所需要的格式
        train_x = train_x.reshape(train_x.shape[0], 1, train_x.shape[1])
        test_x = test_x.reshape(test_x.shape[0], 1, test_x.shape[1])

        return np.array(train_x), np.array(train_y), np.array(test_x), np.array(test_y)

    def max_Min(self,data):
        """
        对数据进行归一化处理
        :param dataset:
        :return:
        """
        d1 = data.shape[0]
        d2 = data.shape[1]
        for i in range(d2):
            Max = max(data[:, i])
            Min = min(data[:, i])
            for j in range(d1):
                data[j, i] = (data[j, i] - Min) / (Max - Min)
        print(data)
        return data

    def split_dataset_train_valid(self,data, ratio=0.8, timestep=1):
        """
        主要是将数据集分割为训练集和验证集
        :param dataset:
        :param ratio:
        :return:
        """
        data = np.loadtxt(data, dtype=np.float64)
        train_size = int(len(data) * ratio)  # 训练集的大小
        train_dataset = data[:train_size]
        valid_dataset = data[train_size:]

        train_dataset_X, train_dataset_Y, valid_dataset_X, valid_dataset_Y = [], [], [], []
        for i in range(len(train_dataset) - timestep):
            x = train_dataset[i:i + timestep]
            train_dataset_X.append(x)
            train_dataset_Y.append(train_dataset[i + timestep])
        for j in range(len(valid_dataset) - timestep):
            x = valid_dataset[j:j + timestep]
            valid_dataset_X.append(x)
            valid_dataset_Y.append(valid_dataset[j + timestep])

        train_dataset_X = np.array(train_dataset_X)
        train_dataset_Y = np.array(train_dataset_Y)
        valid_dataset_X = np.array(valid_dataset_X)
        valid_dataset_Y = np.array(valid_dataset_Y)

        train_dataset_X = np.reshape(train_dataset_X, newshape=[-1, timestep, train_dataset_X.shape[1]])
        valid_dataset_X = np.reshape(valid_dataset_X, newshape=[-1, timestep, valid_dataset_X.shape[1]])

        return train_dataset_X, train_dataset_Y, valid_dataset_X, valid_dataset_Y


if __name__=='__main__':
    dp=Data_Processing()
    count=dp.count_0_num(['morning.csv','shangwu.csv','afternoon.csv','evening_dataset.csv'],'measureTime')
    print(count)
    del count
    count=dp.count_0_num('morning.csv','measureTime')
    print(count)






