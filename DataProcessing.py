"""-*- coding: utf-8 -*-
 DateTime   : 2018/10/4 20:35
 Author  : Peter_Bonnie
 FileName    : DataProcessing.py
 Software: PyCharm
"""
import pandas as pd
import numpy as np
import os
import time

col_names_chinese = ["空气温度", "空气湿度", "土壤温度", "土壤湿度", "土壤导电率", "光照度", "风速", "风向", "土壤PH", "负氧离子浓度", \
                     "雨量", "紫外辐射", "大气压", "光合辐射", "日照时数", "空气二氧化碳", "盐分", "水溶解氧", "水溶解二氧化碳", "土壤温度-5cm", \
                     "土壤湿度-5cm", "土壤温度-15cm", "土壤湿度-15cm", "土壤温度-35cm", "土壤湿度-35cm", "水温度", "水PH"]
col_names_english = ["air_temp", "air_humidity", "land_temp", "land_humidity", "land_conduct", "light", "wind_sp",
                     "wind_direct", \
                     "land_PH", "neg_oxy_ion_concent", "rainy_num", "ultraviolet_radiation", "atm_pres",
                     "photosynthetic_rad", \
                     "sunshine_hours", "air_CO2", "salt", "water_dissolved_oxy", "water_dissolved_CO2", "land_temp-5cm",
                     "land_hum-5cm", \
                     "land_temp-15cm", "land_hum-15cm", "land_temp-35cm", "land_hum-35cm", "water_temp", "water_PH"]


class Config(object):
    """
    中文到英文字段的映射
    """
    def __init__(self,col_names=[]):
        """
        配置一些简单的属性
        :param col_names:
        """
        self.col_names=col_names


class DataProcessing(object):
    """
    数据处理的类，主要是用于来处理数据的查询，清洗
    """
    def __init__(self):
        self.path="Data_Orginal/"

    def merge_data(self,list_csv=[]):
        """
        合并多个csv文件，返回一个总的文件
        :param list:
        :return:
        """
        file_size=len(list_csv)
        if file_size==0:
            raise ValueError("list_csv is empty.Please input some file.")
        else:
            df = pd.DataFrame()
            file_name=[]
            for j in range(file_size):
                file_name.append(list_csv[j].split('.')[0].split('/')[1])
            for  i,key in enumerate(file_name):
                data=pd.read_csv(list_csv[i],low_memory=False,header=None)
                values=data.values
                col=data.columns
                df[key]=values[1:].reshape(-1,)
            df.to_csv("process_data.csv",index=False)
        return " merge data has been succed"

    def get_csv_by_TargetId(self,data):
        """
        将同一targetId的数据放在一起，这样形成不同的字段，并生成多个csv文件。
        :param data:
        :return:
        """
        temp_data=pd.read_csv(data,low_memory=False)
        # 生成35个嵌套表来存储35个特征值
        for i in range(1,36,1):
            temp_data[temp_data['targetId']==i].to_csv(str(i)+".csv",index=False)

        print("get data successfully.")

    def  set_col_Names(self,data,col_names=[]):
        """
        设置列属性
        :param data:
        :param col_names:
        :return:
        """
        pass

    # @staticmethod
    def single_rename_col_name(self,data,col_old_name,col_new_name):
        """
        为单个csv文件的列属性重命名
        :param data:
        :return:
        """
        temp_data=pd.read_csv(data)
        temp_data=pd.DataFrame(temp_data)
        temp_data.rename(columns={col_old_name:col_new_name},inplace=True)
        #这里将Id，STId,TargetId去掉
        temp_data.drop("Id",axis=1,inplace=True)
        temp_data.drop("STId",axis=1,inplace=True)
        temp_data.drop("targetId",axis=1,inplace=True)

        temp_data.to_csv(data,index=False)

    def mul_rename_col_name(self,col_old_name,col_new_name):
        """
        批量修改csv文件列属性名字
        :param data:
        :param col_old_name:
        :param col_new_name:
        :return:
        """
        for i,name in zip(range(1,28,1),col_new_name):
            self.single_rename_col_name(data="Data_Pro/"+str(i)+".csv",col_old_name=col_old_name,col_new_name=name)

    def process_time(self):
        """
        将时间属性秒后面的小数点去掉，然后再将数据保存起来
        :param data:
        :return:
        """
        for i,name in zip(range(1,28,1),col_names_english):
            df=pd.read_csv("Data_Pro/"+str(i)+".csv")
            df_1=pd.DataFrame()
            temp=[time.split('.')[0] for time in list(df['measureTime'].values)]
            df_1['measureTime']=temp
            df_1[name]=df[name]
            print(temp)
            df_1.to_csv(str(i)+".csv",index=False)

    #现在合并这块出了点问题，等过段时间再弄。
    def  merge_csv_by_same_MeasureTime(self,merge_file,on=['measureTime'],how="outer",org_csv=[]):
        """
        通过时间特征将多个csv文件放在一起
        :param merge_file:
        :param on:
        :param how:
        :param from_csv：
        :return:
        """
        if len(org_csv)==0:
            raise ValueError("No file input.")
        elif len(org_csv)==1:
            print("there is no file need to merge.")
        else:
            temp_file=pd.read_csv("Data_Pro/"+org_csv[0],low_memory=False)
            temp_file.drop_duplicates(inplace=True)
            temp_file.to_csv("Data_Pro/"+merge_file,index=False)
            for i in range(1,len(org_csv),1):
                temp_file_1=pd.read_csv("Data_Pro/"+org_csv[i],low_memory=False)
                temp_file_1.drop_duplicates(inplace=True)
                temp_file=pd.DataFrame(temp_file_1)
                merge_file=pd.read_csv("Data_Pro/"+merge_file,low_memory=False)
                merge_file=pd.DataFrame(merge_file)
                pd.merge(merge_file,temp_file_1,how=how,on=on).to_csv("Data_Pro/"+merge_file,index=False)

#主函数
def main():
    # 常量设置
    dp=DataProcessing()
    # list_csv=os.listdir("Data_Pro")
    # dp.mul_rename_col_name(col_old_name="measureData",col_new_name=col_names_english)
    # dp.merge_csv_by_same_MeasureTime("merge.csv",on=['measureTime'],how="left",org_csv=["a18.csv","a19.csv"])
    org_csv=["a20.csv","a21.csv","a22.csv","a23.csv","a24.csv","a25.csv"]
    temp_file=pd.read_csv("Data_Pro/"+org_csv[0])
    temp_file.drop_duplicates(['measureTime'],inplace=True)
    temp_file=pd.DataFrame(temp_file)
    temp_file.to_csv("Data_Pro/merge.csv",index=False)
    for i in range(1,len(org_csv),1):
        temp_file_1=pd.read_csv("Data_Pro/"+org_csv[i])
        temp_file_1.drop_duplicates(['measureTime'],inplace=True)
        temp_file_1=pd.DataFrame(temp_file_1)
        merge=pd.read_csv("Data_Pro/merge.csv")
        merge.drop_duplicates(['measureTime'],inplace=True)
        merge=pd.DataFrame(merge)
        pd.merge(merge,temp_file_1,how="inner",on=['measureTime']).to_csv("Data_Pro/merge.csv",index=False)

if __name__=="__main__":
    main()































