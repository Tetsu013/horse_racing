# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import svm
import pandas as pd
import numpy as np
import csv
import MySQLdb
from sshtunnel import SSHTunnelForwarder
from time import sleep
import codecs, sys

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

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

def id_name():
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    arr=np.empty((0,2), str)
    sql = "SELECT m.horse_id, m.horse_name "
    sql += "FROM m_horse AS m "
    #sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
    #sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        id = np.array([])
        url = np.array([])
  
        for row in rows:
            column = np.array([])
            column = np.append(column, row[0])
            column = np.append(column, row[1])
            
            arr = np.append(arr, np.array([column]), axis=0)

    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)
    connection.commit()
    StopSSHSession(server, connection)
    print(arr)
    f = open('out_horse_name.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    for i in arr:
        writer.writerow(i)
    f.close()
    return arr
if __name__ == "__main__":
    id_name()
