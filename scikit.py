# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import svm
import pandas as pd
import numpy as np
import csv
import MySQLdb
from sshtunnel import SSHTunnelForwarder
from time import sleep


def Svm(arr, arr3):
    
    target, training = np.hsplit(arr, [1])
    print(len(target), len(training))
    tar2= np.ravel(target.T)
    clf = svm.SVC(gamma=0.001, C=1.)
    print(tar2)
    #svmのモデル生成(学習)fit
    print(arr3)
    #svmの学習
    #clf.fit(training[:test_index], tar2[:test_index])
    clf.fit(training, tar2)
    #テスト(予測) けつtest_index個分のテスト
    #print(np.array(clf.predict(training[test_index:])))
    print(np.array(clf.predict(arr3)))

#馬勝率・騎手勝率の計算(例は馬のみ、騎手も同様)
#input
"""
[
[馬Aのid,  騎手Aのid]
[馬Bのid,  騎手Bのid]
[馬Cのid,  騎手Cのid]
 .
 .
 .
[馬Zのid,  騎手Zのid]
]
"""
#output
"""
[
 [馬Aのid,  馬Aの勝率]
 [馬Bのid,  馬Bのid]
 [馬Cのid,  馬Cのid]
 .
 .
 .
 [馬Zのid,  馬Zのid]
 ]
"""
def Num(arr2):
    horse, jokey = np.hsplit(arr2, [1])
    horse2= np.ravel(horse.T)
    jokey2= np.ravel(jokey.T)
    horse_zisyo = np.empty((0,2), float)
    jokey_zisyo = np.empty((0,2), float)
    
    for i in horse2:
        zisyo =  np.array([])
        zisyo = np.append(zisyo, i)
        zisyo = np.append(zisyo, (len(np.where(horse2==i)[0])*1.0) / (len(arr2)*1.0))
        horse_zisyo = np.append(horse_zisyo, np.array([zisyo]), axis=0)
    for i in jokey2:
        zisyo2 =  np.array([])
        zisyo2 = np.append(zisyo2, i)
        zisyo2 = np.append(zisyo2, (len(np.where(jokey2==i)[0])*1.0) / (len(arr2)*1.0))
        jokey_zisyo = np.append(jokey_zisyo, np.array([zisyo2]), axis=0)
    for a in horse_zisyo:
        a[1] = a[1] / max(horse_zisyo[:,1])
    for b in jokey_zisyo:
        b[1] = b[1] / max(jokey_zisyo[:,1])

    return horse_zisyo, jokey_zisyo

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

def make_training(arr, arr3, horse, jockey):
    #print(arr)

    if max(arr[:,1]) >= max(arr3[:,0]):
        ma = max(arr[:,1])
    else:
        ma = max(arr3[:,0])

    if max(arr[:,4]) >= max(arr3[:,3]):
        mb = max(arr[:,4])
    else:
        mb = max(arr3[:,3])
    for ar in arr:
 
        ab = list(np.where(horse[:,0]==ar[1]))
        ac = list(np.where(jockey[:,0]==ar[2]))
        for io in list(ab[0]):
            ar[1] = horse[int(io)][1]
        for ip in list(ac[0]):
            ar[2] = jockey[int(ip)][1]

        ar[3] = (ar[3]*100.0) / (ma)
        ar[4] = (ar[4]*0.1) / (mb)
    for ar3 in arr3:
     
        ab = list(np.where(horse[:,0]==ar3[0]))
        ac = list(np.where(jockey[:,0]==ar3[1]))
        if len(list(ab[0])) == 0:
            ar3[0] = 0.0
        else:
            for io in list(ab[0]):
                ar3[0] = horse[int(io)][1]
        if len(list(ac[0])) == 0:
            ar3[1] = 0.0
        else:
            for ip in list(ac[0]):
                ar3[1] = jockey[int(ip)][1]

        ar3[2] = (ar3[2]*100.0) / (ma)
        ar3[3] = (ar3[3]*0.1) / (mb)

    print(arr)
    return arr, arr3


if __name__ == "__main__":
    
    
    arr=np.empty((0,5), float)
    arr2=np.empty((0,2), float)
    
    arr3=np.empty((0,4), float)
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    
    sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, basis_weight "
    sql += "FROM t_keiba_data_test AS tkd "
    sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    
    sql2 = "SELECT tkd.horse_name_id, tkd.jockey_id "
    sql2 += "FROM t_keiba_data_test AS tkd "
    sql2 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql2 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id "
    sql2 +=	"WHERE tkd.score = 1"

    sql3 = "SELECT tkd.id, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, basis_weight "
    sql3 += "FROM t_keiba_info AS tkd "
    sql3 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql3 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
 
    
    
    
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        cursor.execute(sql2)
        rows2 = cursor.fetchall()
        
        cursor.execute(sql3)
        rows3 = cursor.fetchall()

        for row3 in rows3:
            cc = np.array([])
            cc = np.append(cc, row3[1]*1.0)
            cc = np.append(cc, row3[2]*1.0)
            cc = np.append(cc, row3[4]*1.0)
            cc = np.append(cc, row3[5]*1.0)
            arr3 = np.append(arr3, np.array([cc]), axis=0)
        arr3, abc = np.vsplit(arr3, 2)

        for row2 in rows2:
            
            col = np.array([])
            col = np.append(col, row2[0]*1.0)
            col = np.append(col, row2[1]*1.0)
            arr2 = np.append(arr2, np.array([col]), axis=0)
        for row in rows:
            column = np.array([])
            column = np.append(column, row[1]*1.0)
            column = np.append(column, row[2]*1.0)
            column = np.append(column, row[3]*1.0)
            column = np.append(column, row[5]*1.0)
            column = np.append(column, row[6]*1.0)

            arr = np.append(arr, np.array([column]), axis=0)
            '''
                print(row[0])		# score
                print(row[1])		# horse_rank
                print(row[2])		# horse_name_id
                print(row[3])		# jockey_id
                print(row[4])		# horse_sex
                print(row[5])		# horse_year
                print(row[6])       # basis_weight
                '''
    
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)
    hor, joc = Num(arr2)
    new_arr, new_arr3 = make_training(arr, arr3, hor, joc)
    connection.commit()
    StopSSHSession(server, connection)
    print(arr)
    Svm(new_arr,new_arr3)