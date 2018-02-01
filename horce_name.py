# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import svm
import pandas as pd
import numpy as np
import csv
import MySQLdb
from sshtunnel import SSHTunnelForwarder
from time import sleep
"""
import codecs, sys

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
"""
#馬勝率・騎手勝率の計算(例は馬のみ、騎手も同様)
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

def sql_horce_name(id):
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    
    sql = "SELECT horse_id, horse_name from m_horse "
    sql +=	"	WHERE horse_id = "
    sql += id

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
            print(row[0])
            print(type(row[1]))
            print(row[1])
            #print(row[1].decode())
            
            #print(row[1].encode("utf-8"))
            #horse = row[1].encode("utf-8")
            horse = row[1]
        return horse.encode("utf-8")
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)

if __name__ == "__main__":
    
    
    arr=np.empty((0,3), float)
    arr2=np.empty((0,2), float)
    
    arr3=np.empty((0,3), float)
    server = StartSSHSession()
    connection = GetConnection(server.local_bind_port)
    cursor = connection.cursor()
    
    sql = "SELECT horse_id, horse_name from m_horse "
    sql +=	"	WHERE horse_id = 2578 or horse_id = 3438 or horse_id = 1163"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            print(row[1].encode("utf-8"))
            print(row)
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)
