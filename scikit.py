# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import csv
import MySQLdb
import sql_horse_name
from sshtunnel import SSHTunnelForwarder
from time import sleep
from basic_wins import Num
from basic_wins import make_training_one
from basic_wins import Com
from basic_wins import Aska
from horce_name import sql_horce_name

#SVMによる予測順位
def Svm(arr, arr3):
    target, training = np.hsplit(arr, [1])
    tar2= np.ravel(target.T)
    
    #parameters = [{'kernel':['rbf'], 'C':np.logspace(1, 10, 10), 'gamma':np.logspace(10, 1000, 50)}]
                  #{'kearnel':('rbf'), 'C':np.logspace(-4, 4, 9)} ]
    #clf = GridSearchCV(svm.SVC(), parameters)
    
    clf = svm.SVC(gamma=10000000000.0, C=10.)
   
    clf.fit(training, tar2)
    
    print(clf)
    #print(clf.best_estimator_)

    return np.array(clf.predict(arr3))

def StartSSHSession():
    server = SSHTunnelForwarder(
                                ('yuruhuwa-bourg.sakura.ne.jp', 22),
                                ssh_username="yuruhuwa-bourg",
                                ssh_password="eh4uat56gu",
                                remote_bind_address=('mysql541.db.sakura.ne.jp', 3306)
                                )
    server.start()
    return server


def GetConnection(port):
    connection = MySQLdb.connect(
                                 host='127.0.0.1',
                                 port=port,
                                 user='yuruhuwa-bourg', 
                                 passwd='1q2w3e4r', 
                                 db='yuruhuwa-bourg_keiba', 
                                 charset='utf8')
    return connection

def StopSSHSession(server, connection):
    connection.close()
    server.stop()

def Aska_method(a):
    finResult = np.empty((0,3), float)
    print(a)
    for i in a:
        array = np.array([])
        key = str(i[0])
        key = key.replace(".0", "")
        try:
            array = np.append(array, i[0])
            array = np.append(array, i[1])
            array = np.append(array, Aska(key))
        except:
            array = np.append(array, 0.0)
            print("errors")
        print(len(array))
        finResult = np.append(finResult, np.array([array]), axis = 0)

    return finResult
#各データを正規化する
def make_training(arr, arr3):

    if max(arr[:,1]) >= max(arr3[:,0]):
        ma = max(arr[:,1])
    else:
        ma = max(arr3[:,0])

    if max(arr[:,2]) >= max(arr3[:,1]):
        mb = max(arr[:,2])
    else:
        mb = max(arr3[:,1])

    if max(arr[:,3]) >= max(arr3[:,2]):
        mc = max(arr[:,3])
    else:
        mc = max(arr3[:,2])

    for ar in arr:
        ar[1] = (ar[1]) / (ma)
        ar[2] = (ar[2]) / (mb)
        ar[3] = (ar[3]) / (mc)

    for ar3 in arr3:
        ar3[0] = (ar3[0]) / (ma)
        ar3[1] = (ar3[1]) / (mb)
        ar3[2] = (ar3[2]) / (mc)

    print(arr)
    return arr, arr3

if __name__ == "__main__":
    

    finResult = np.empty((0,3), float)
    
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)

    cursor = connection.cursor()
    
    #学習用データセット作成
    sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, tkd.basis_weight, tkd.trainer_id, tkd.popularity, tkd.url "
    sql += "FROM t_keiba_data_result AS tkd "
    sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql +=	"LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id "
    sql +=	"LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
    
    print(sql)
    
    sql2 = "SELECT tkd.horse_name_id, tkd.jockey_id, tkd.trainer_id "
    sql2 += "FROM t_keiba_data_result AS tkd "
    sql2 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql2 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id "
    sql2 +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
    sql2 +=	" WHERE tkd.score = 1"
    
     #テスト用データセット作成
    sql3 = "SELECT tkd.id, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, tkd.basis_weight, tkd.url, tkd.trainer_id, tkd.popularity "
    sql3 += "FROM t_keiba_predata AS tkd "
    sql3 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql3 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    sql3 +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
    sql3 +=	"   WHERE tkd.url = 201705050811"
    #sql3 +=	"   WHERE tkd.url = 201708050812"

    print(sql3)
    try:
        cursor.execute(sql)
        selectSVM = cursor.fetchall()
        
        cursor.execute(sql2)
        selectWinRate = cursor.fetchall()
        
        cursor.execute(sql3)
        selectSVM2 = cursor.fetchall()
        
        id = np.array([])
        url = np.array([])
        
        
        
        race_predata = np.empty((0,3), float)
        win_array2   = np.empty((0,4), float)
        
        
        for row3 in selectSVM2:
            key_place = (row3[6])[4:6]
            cc = np.array([])
            ccc = np.array([])
            id = np.append(id, row3[1])
            cc = np.append(cc, row3[4]*1.0)
            cc = np.append(cc, row3[5]*1.0)
            cc = np.append(cc, row3[8]*1.0)
            ccc = np.append(ccc, row3[0]*1.0)
            ccc = np.append(ccc, row3[1]*1.0)
            ccc = np.append(ccc, row3[2]*1.0)
            ccc = np.append(ccc, row3[7]*1.0)

            win_array2 = np.append(win_array2, np.array([ccc]), axis=0)
            race_predata = np.append(race_predata, np.array([cc]), axis=0)

        race_result  = np.empty((0,4), float)
        win_array    = np.empty((0,4), float)
        for row in selectSVM:
            place = (row[9])[4:6]
            if place == key_place:
                column = np.array([])
                win_column = np.array([])
                column = np.append(column, row[1]*1.0)
                column = np.append(column, row[5]*1.0)
                column = np.append(column, row[6]*1.0)
                column = np.append(column, row[8]*1.0)
                win_column = np.append(win_column, row[1]*1.0)
                win_column = np.append(win_column, row[2]*1.0)
                win_column = np.append(win_column, row[3]*1.0)
                win_column = np.append(win_column, row[7]*1.0)
                race_result = np.append(race_result, np.array([column]), axis=0)
                win_array = np.append(win_array, np.array([win_column]), axis=0)

        win_rate = np.empty((0,3), float)
        for row2 in selectWinRate:
            col = np.array([])
            col = np.append(col, row2[0]*1.0)
            col = np.append(col, row2[1]*1.0)
            col = np.append(col, row2[2]*1.0)
            win_rate = np.append(win_rate, np.array([col]), axis=0)

    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)

    new_arr, new_arr3 = make_training(race_result, race_predata)

    hor, joc, tra = Num(win_rate)
    arr3_copy = np.array(win_array)
    new_arr_rate, new_arr3_rate = make_training_one(win_array2, win_array, hor, joc, tra)
    connection.commit()
    StopSSHSession(server, connection)
    sss = Com(new_arr3_rate,arr3_copy)
    basicwins = dict(sss)
    print(sss)
    print("-----------------------")
    print(basicwins)


    #ここからSVMゾーン
    print(new_arr)
    print(new_arr3)
    uma = Svm(new_arr,new_arr3)

    print(np.hstack((id.reshape(len(id),1),uma.reshape(len(uma),1))))
    wk = np.hstack((id.reshape(len(id),1),uma.reshape(len(uma),1)))
    s = sorted(list(wk),key=lambda i:i[1])

    #結果を出力
    f = open('20171125_kyoto3_ask.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    #福田メソッド

    for i in s:
        array = np.array([])
        try:
            print(i[0])
            print(basicwins[i[0]])
            array = np.append(array, i[0])
            array = np.append(array, i[1])
            array = np.append(array, basicwins[i[0]])
            writer.writerow(str(i[0])+":"+str(i[1])+":"+str(basicwins[i[0]]).replace(',', ''))
        except:
            array = np.append(array, i[0])
            array = np.append(array, i[1])
            array = np.append(array, 0.0)
            print("errors")
            writer.writerow(str(i[0])+":"+str(i[1])+":"+str(0.0).replace(',', ''))
        finResult = np.append(finResult, np.array([array]), axis = 0)
    print(finResult)
    
    #あすかメソッド
    """
    for i in Aska_method(s):
        a = sql_horce_name(str(i[0]).encode("utf-8").replace(".0", ""))
        writer.writerow(str(i[0])+":"+str(i[1])+":"+str(i[2]).replace(',', ''))
    """
    # ファイルクローズ
    f.close()

    print("finish")