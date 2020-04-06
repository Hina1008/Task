import os
import sys
import datetime as dt
import pandas as pd 
import numpy as np
import locale

#アクセスログの存在する年
s_year = 2000
e_year = 2020

#ホストネームに対するアクセス数
Host_access = {}

#月対応表
Month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
Month_dic = dict(zip([i for i in range(1,13)], Month))
Month_dic2 = dict(zip(Month, [i for i in range(1,13)]))

#MultiIndex作成
def create_dataframe(array,name):
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=name)
    series = pd.Series(0, index=index)
    return pd.DataFrame(series)

##########年-月-日-時間のデータフレーム作成#################################
#月だけ個別作成1→"Jan"に変換
Month_val = sorted([i for i in range(1,13)]*31*24)*(e_year-s_year+1)
Month_str = [Month_dic[Month_val[i]] for i in range(len(Month_val))]
col_name=['Year','Month','Date','Time']
arrays = [sorted([i for i in range(s_year,e_year+1)]*31*24*12),\
          Month_str,\
          sorted([i for i in range(1,32)]*24)*(e_year-s_year+1)*31,\
          [str(dt.time(hour=i, minute=0, second=0)) for i in range(24)]*31*12*(e_year-s_year+1)]
df1 = create_dataframe(arrays,col_name)
#############################################################



def Host(host_name):
    global Host_access
    if host_name in Host_access:
        Host_access[host_name] += 1
    else:
        Host_access[host_name] = 1

def Date_proc(name, date):
    global  df1, df2
    date2 = date[2].split(":")
    year = date2[0]
    hour = date2[1]
    time = str(dt.time(hour=int(hour), minute=0, second=0))
    #Dataframeにアクセス数を加算
    df1.loc[(int(year), date[1], int(date[0]), time),0] += 1
    #Dataframeに名前がなければ追加、あればアクセス数加算
    if name in Host_access:
        df1.loc[(int(year), date[1], int(date[0]),time), name] += 1
    else:
        df1[name] = 0
        df1.loc[(int(year),date[1],int(date[0]),time),name] += 1

#データ加工
def Data(path):
    with open(path) as f:
        lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        #リモートホスト,アクセス時間を抽出
        for each_log in lines_strip:
            coffee = each_log.split(" ")
            #日時の記法加工 & 時間帯別アクセス数を書き込む
            Date_proc(coffee[0], coffee[3].strip("[").split("/"))
            #リモートホストに対するアクセス数を計算
            Host(coffee[0])

if __name__ == '__main__':
	#ログのファイル名を取得する
    files = sys.argv

    #ログファイルを指定しているかどうか
    if (len(files) < 2):
        print ("ログファイルを入力してください")
        quit()

    #抽出する期間を入力
    print("抽出する期間を指定してください")
    start = input("始まり(例 2017/4/1/):").split("/")
    end = input("終わり(例 2017/4/30):").split("/")
    start = [int(i) for i in start]
    end = [int(i) for i in end]

    #期間の指定が正しいか
    if len(start) != 3 or len(end) != 3:
        print("例通りに入力してください")
        quit()
    elif start[0] < s_year or end[0] > e_year or s_year > e_year or\
         start[1] < 1 or start[1] > 12 or end[1] < 1 or end[1] > 12 or\
         start[2] < 1 or start[2] > 31 or end[2] < 1 or end[2] > 31:
        print("期間の指定を入力し直してください")
        quit()

    #期間のIndex番号
    s_num = (int(start[0])-s_year)*24*31*12+int(start[1])*24*31+int(start[2])*24+0-24*31-24
    e_num = (int(end[0])-s_year)*24*31*12+int(end[1])*24*31+int(end[2])*24+23-24*31-24+1


    #ログファイル複数読み取り
    for i in range(1,len(files)):
        path = files[i]
        if(os.path.exists(path) == True):		
            print ("現在処理中のファイル名:" + path)
        else:
            print ("存在しないファイルです。ファイル名:" + path)
            continue
        #ログアクセス回数の集計 
        Data(path)
    
    #指定した期間を抽出
    df1 = df1.rename(columns={0: 'Total_AC'})#合計アクセス回数にラベル変更
    d= df1[s_num:e_num].to_dict(orient="list")#各ホストの時間帯アクセス数をリスト化
    df2 = df1[s_num:e_num]  #指定した期間を抽出

    #データフレーム作成###############
    Host_name_list = list(Host_access.keys())
    df2 = df2.drop(Host_name_list, axis = 1)
    Rank = ["No."+str(i) for i in range(1,len(Host_name_list)+1)] #
    Name = ["AC"+str(i) for i in range(1,len(Host_name_list)+1)]
    column = [None]*(len(Rank)+len(Name))
    column[::2] = Rank
    column[1::2] = Name
    for i in column:
        df2[i] = None
    #print(df2)
    ##################################

    #時間帯アクセス回数をソートして、作成したデータフレームに挿入##################
    for i in range(e_num - s_num):
        dic = dict(zip(Host_name_list,[d[j][i] for j in Host_name_list]))
        dic = sorted(dic.items(), key=lambda x:x[1], reverse=True)
        for j in range(len(column)):
            if j%2:
                df2.at[df2.index[i],column[j]] = dic[int(j/2)][1]
            else:
                df2.at[df2.index[i],column[j]] = dic[int(j/2)][0]
    #####################################################################
    #df2.to_csv("access_log_ana_result.csv")
    print(df2)
