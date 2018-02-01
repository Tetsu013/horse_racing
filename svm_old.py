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

#SVMによる予測順位
def Svm(arr, arr3):
    target, training = np.hsplit(arr, [1])
    tar2= np.ravel(target.T)
    
    parameters = [{'kernel':['rbf'], 'C':np.logspace(1, 10, 10), 'gamma':np.logspace(10, 1000, 50)}]
    #{'kearnel':('rbf'), 'C':np.logspace(-4, 4, 9)} ]
    
    #clf = GridSearchCV(svm.SVC(), parameters)
    #clf.fit(training, tar2)
    
    # clf2=svm.SVC(class_weight='balanced', random_state=0)
    #param_range=[0.01, 0.1, 1.0] #変化させるパラメータに設定する値たち
    #param_grid=[{'C':param_range,'kernel':['rbf', 'linear'], 'gamma':param_range}] #Cとカーネルとgammaを変化させて最適化させる
    
    #グリッドサーチにより最適値を求める
    #gs=grid_search.GridSearchCV(estimator=clf2, param_grid=param_grid, scoring='accuracy', cv=10, n_jobs=-1)
    #gs=gs.fit(X_train,train_label)
    
    
    clf = svm.SVC(gamma=0.0001, C=1000.)
    clf.fit(training, tar2)
    #print(clf.best_estimator_)
    #svmのモデル生成(学習)fit
    print(arr3)
    #svmの学習
    
    
    print(np.array(clf.predict(arr3)))
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
    
    for ar in arr:
        ar[1] = (ar[1]) / (ma)
        ar[2] = (ar[2]) / (mb)
    
    for ar3 in arr3:
        ar3[0] = (ar3[0]) / (ma)
        ar3[1] = (ar3[1]) / (mb)
    
    print(arr)
    return arr, arr3

if __name__ == "__main__":
    
    
    result=np.empty((0,3), float)
    predata=np.empty((0,2), float)
    
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    
    #学習用データセット作成
    sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, basis_weight "
    sql += "FROM t_keiba_data_result AS tkd "
    sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    
    #テスト用データセット作成
    sql3 = "SELECT tkd.id, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, basis_weight, url "
    sql3 += "FROM t_keiba_predata AS tkd "
    sql3 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql3 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    sql3 +=	"   WHERE tkd.url = 201708050412"
    
    
    
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        cursor.execute(sql3)
        rows3 = cursor.fetchall()
        
        id = np.array([])
        url = np.array([])
        
        for row3 in rows3:
            cc = np.array([])
            id = np.append(id, row3[1])
            cc = np.append(cc, row3[4]*1.0)
            cc = np.append(cc, row3[5]*1.0)
            #url= np.append(cc, row3[6]*1.0)
            print(row3[6])
            predata = np.append(predata, np.array([cc]), axis=0)
        
        for row in rows:
            column = np.array([])
            column = np.append(column, row[1]*1.0)
            column = np.append(column, row[5]*1.0)
            column = np.append(column, row[6]*1.0)
            result = np.append(result, np.array([column]), axis=0)

    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)

    new_arr, new_arr3 = make_training(result, predata)
    connection.commit()
    StopSSHSession(server, connection)
    uma = Svm(new_arr,new_arr3)
    print(id)
    print(url)
    print(np.hstack((id.reshape(len(id),1),uma.reshape(len(uma),1))))
    wk = np.hstack((id.reshape(len(id),1),uma.reshape(len(uma),1)))
    s = sorted(list(wk),key=lambda i:i[1])
    print(s)
    f = open('svm.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    aio = []
    for i in s:
        writer.writerow((str(i[0])+":"+str(i[1])).replace(',', '') )
# ファイルクローズ
f.close()