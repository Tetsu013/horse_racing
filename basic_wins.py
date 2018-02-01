# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import svm
import pandas as pd
import numpy as np
import csv
import MySQLdb
from sshtunnel import SSHTunnelForwarder
from time import sleep

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
    horse, jokey, trainer = np.hsplit(arr2, [1,2])
    horse2= np.ravel(horse.T)
    jokey2= np.ravel(jokey.T)
    trainer2 = np.ravel(trainer.T)
    horse_zisyo = np.empty((0,2), float)
    jokey_zisyo = np.empty((0,2), float)
    trainer_zisyo = np.empty((0,2),float)
    
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
    for i in trainer2:
        zisyo3 =  np.array([])
        zisyo3 = np.append(zisyo3, i)
        zisyo3 = np.append(zisyo3, (len(np.where(trainer2==i)[0])*1.0) / (len(arr2)*1.0))
        trainer_zisyo = np.append(trainer_zisyo, np.array([zisyo3]), axis=0)
    for a in horse_zisyo:
        a[1] = a[1] / max(horse_zisyo[:,1])
    for b in jokey_zisyo:
        b[1] = b[1] / max(jokey_zisyo[:,1])
    for c in trainer_zisyo:
        c[1] = c[1] / max(trainer_zisyo[:,1])
    
    return horse_zisyo, jokey_zisyo, trainer_zisyo

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

def make_training_one(arr, arr3, horse, jockey, trainer):
    #print(arr)

    for ar in arr:
        
        ab = list(np.where(horse[:,0]==ar[1]))
        ac = list(np.where(jockey[:,0]==ar[2]))
        ad = list(np.where(jockey[:,0]==ar[3]))
        for io in list(ab[0]):
            ar[1] = horse[int(io)][1]
        for ip in list(ac[0]):
            ar[2] = jockey[int(ip)][1]
        for iq in list(ad[0]):
            ar[3] = trainer[int(iq)][1]

    for ar3 in arr3:
        
        ab = list(np.where(horse[:,0]==ar3[1]))
        ac = list(np.where(jockey[:,0]==ar3[2]))
        ad = list(np.where(trainer[:,0]==ar3[3]))
        
        if len(list(ab[0])) == 0:
            ar3[1] = 0.0
        else:
            for io in list(ab[0]):
                ar3[1] = horse[int(io)][1]
        
        if len(list(ac[0])) == 0:
            ar3[2] = 0.0
        else:
            for ip in list(ac[0]):
                ar3[2] = jockey[int(ip)][1]
        
        if len(list(ad[0])) == 0:
            ar3[3] = 0.0
        else:
            for iq in list(ad[0]):
                ar3[3] = trainer[int(iq)][1]

    return arr, arr3

def Com(arr3,arr_before):
    last = np.empty((0,2), float)
    for ara, iou in zip(arr3, arr_before):
        ccc = np.array([])
        aer = ara[1]+ara[2]
        ccc = np.append(ccc, iou[1])
        ccc = np.append(ccc, aer)
        last = np.append(last, np.array([ccc]), axis=0)
    s = sorted(list(last),key=lambda i:i[1])
    a = np.array(s)
    print(a)
    return a

def Csv(out):
    f = open('svm.csv', 'r')

    reader = csv.reader(f)
    ao = []
    for row in reader:
        print(row)
        row_data = row[0].split(":")
        print(float(row[0].split(":")[0]))
        print(np.where(out == float(row[0].split(":")[0])))
        print(out[np.where(out == float(row[0].split(":")[0]))][0])
        print(out[np.where(out == float(row[0].split(":")[0]))[0]][0][1])
        aioi = row_data[0] + ":" + row_data[1] + ":" + str(out[np.where(out == float(row[0].split(":")[0]))[0]][0][1])
        print(aioi)
        ao.append(aioi)
    f.close()
    print(ao)
    return ao

def Aska(id):
    
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    
    sql = "SELECT winning_rate "
    sql += "FROM calc_winning_rate "
    sql += "WHERE horse_name_id = "
    sql += id

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
            return row[0]

    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)

if __name__ == "__main__":
    
    
    arr=np.empty((0,4), float)
    arr2=np.empty((0,3), float)
    
    arr3=np.empty((0,4), float)
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    
    sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, basis_weight, tkd.trainer_id "
    sql += "FROM t_keiba_data_result AS tkd "
    sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    sql +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
    
    sql2 = "SELECT tkd.horse_name_id, tkd.jockey_id, tkd.trainer_id "
    sql2 += "FROM t_keiba_data_result AS tkd "
    sql2 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql2 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id "
    sql2 +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
    sql2 +=	" WHERE tkd.score = 1"
    
    sql3 = "SELECT tkd.id, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, basis_weight,tkd.trainer_id "
    sql3 += "FROM t_keiba_predata AS tkd "
    sql3 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    sql3 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    sql3 +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
    sql3 += " WHERE tkd.url = 201708050412"
    
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        cursor.execute(sql2)
        rows2 = cursor.fetchall()
        
        cursor.execute(sql3)
        rows3 = cursor.fetchall()
        
        for row3 in rows3:
            cc = np.array([])
            cc = np.append(cc, row3[0]*1.0)
            print(row3[1])
            cc = np.append(cc, row3[1]*1.0)
            cc = np.append(cc, row3[2]*1.0)
            cc = np.append(cc, row3[6]*1.0)
            arr3 = np.append(arr3, np.array([cc]), axis=0)
        
        for row2 in rows2:
            col = np.array([])
            col = np.append(col, row2[0]*1.0)
            col = np.append(col, row2[1]*1.0)
            col = np.append(col, row2[2]*1.0)
            arr2 = np.append(arr2, np.array([col]), axis=0)
        
        for row in rows:
            column = np.array([])
            column = np.append(column, row[1]*1.0)
            column = np.append(column, row[2]*1.0)
            column = np.append(column, row[3]*1.0)
            column = np.append(column, row[7]*1.0)
            
            arr = np.append(arr, np.array([column]), axis=0)
    
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)
    
    hor, joc, tra = Num(arr2)
    print(arr3)
    arr3_copy = np.array(arr3)
    new_arr, new_arr3 = make_training_one(arr, arr3, hor, joc, tra)
    connection.commit()
    StopSSHSession(server, connection)
    sss = Com(new_arr3,arr3_copy)
    print(sss)
    f = open('out_Kyoto3.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    for i in sss:
        writer.writerow(i)
    aio = []
    #for i in Csv(sss):
    #writer.writerow(i)
    # ファイルクローズ
    f.close()

