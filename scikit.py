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
from basic_wins import createWinsRate
from basic_wins import raceBasicWinrate
from basic_wins import Aska
from horce_name import sql_horce_name
import SQLCollection

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
#SVMに使うデータを正規化する
def make_training(test, training):

    if max(test[:,1]) >= max(training[:,0]):
        ma = max(test[:,1])
    else:
        ma = max(training[:,0])

    if max(test[:,2]) >= max(training[:,1]):
        mb = max(test[:,2])
    else:
        mb = max(training[:,1])

    if max(test[:,3]) >= max(training[:,2]):
        mc = max(test[:,3])
    else:
        mc = max(training[:,2])

    for ar in test:
        ar[1] = (ar[1]) / (ma)
        ar[2] = (ar[2]) / (mb)
        ar[3] = (ar[3]) / (mc)

    for ar3 in training:
        ar3[0] = (ar3[0]) / (ma)
        ar3[1] = (ar3[1]) / (mb)
        ar3[2] = (ar3[2]) / (mc)

    return test, training

if __name__ == "__main__":
    
    sqlhorse_jokey_zisyolection = SQLhorse_jokey_zisyolection()

    finResult = np.empty((0,3), float)
    

    #学習用データセット作成
    
    SVMTrainData = sqlhorse_jokey_zisyolection.getTrainData
    #if SVMTrainData==-1:
    #   return 0
    
    #上位3位の馬と騎手のデータ
    Top3HorseAndJockeyData = sqlhorse_jokey_zisyolection.getTop3HorseAndJockey
    #if Top3HorseAndJockeyData ==-1:
    #   return 0

    #テスト用データセット作成
    SVMTestData = sqlhorse_jokey_zisyolection.getTestData
    #if( SVMTestData ==-1):
    #   return 0
        
    
    print(sql)
    
    
    
     #テスト用データセット作成
    
    #sql3 +=	"   WHERE tkd.url = 201708050812"

    print(sql3)
    try:
        cursor.execute(sql)
        #SVMTrainData = cursor.fetchall()
        
        cursor.execute(sql2)
        selectWinRate = cursor.fetchall()
        
        cursor.execute(sql3)
        SVMTestData = cursor.fetchall()
        
        horseNameID= np.array([])
        url = np.array([])
        
        race_predata = np.empty((0,3), float)
        basic_wins_test_in   = np.empty((0,4), float)
        
        #テストデータをSVM用とbasic_wins用に格納
        for row3 in SVMTestData:
            key_place = (row3[6])[4:6]
            svm_test = np.array([])
            top3_horce_jokey = np.array([])
            horseNameID= np.append(horseNameID, row3[1])
            svm_test = np.append(svm_test, row3[4]*1.0)
            svm_test = np.append(svm_test, row3[5]*1.0)
            svm_test = np.append(svm_test, row3[8]*1.0)
            top3_horce_jokey = np.append(top3_horce_jokey, row3[0]*1.0)
            top3_horce_jokey = np.append(top3_horce_jokey, row3[1]*1.0)
            top3_horce_jokey = np.append(top3_horce_jokey, row3[2]*1.0)
            top3_horce_jokey = np.append(top3_horce_jokey, row3[7]*1.0)

            basic_wins_in = np.append(win_array2, np.array([top3_horce_jokey]), axis=0)
            race_predata = np.append(race_predata, np.array([svm_test]), axis=0)

        race_result  = np.empty((0,4), float)
        basic_wins_train_in   = np.empty((0,4), float)

        for row in SVMTrainData:
            place = (row[9])[4:6]
            if place == key_place:
                svm_trainning = np.array([])
                top3_horce_jokey_trainning = np.array([])
                svm_trainning = np.append(svm_trainning, row[1]*1.0)
                svm_trainning = np.append(svm_trainning, row[5]*1.0)
                svm_trainning = np.append(svm_trainning, row[6]*1.0)
                svm_trainning = np.append(svm_trainning, row[8]*1.0)
                top3_horce_jokey_trainning = np.append(top3_horce_jokey_trainning, row[1]*1.0)
                top3_horce_jokey_trainning = np.append(top3_horce_jokey_trainning, row[2]*1.0)
                top3_horce_jokey_trainning = np.append(top3_horce_jokey_trainning, row[3]*1.0)
                top3_horce_jokey_trainning = np.append(top3_horce_jokey_trainning, row[7]*1.0)
                race_result = np.append(race_result, np.array([svm_trainning]), axis=0)
                basic_wins_train_in = np.append(win_array, np.array([top3_horce_jokey_trainning]), axis=0)

        win_rate_zisyo = np.empty((0,3), float)

        for row2 in Top3HorseAndJockeyData:
            horse_jokey_trainer_zisyo = np.array([])
            horse_jokey_trainer_zisyo = np.append(horse_jokey_zisyo, row2[0]*1.0)
            horse_jokey_trainer_zisyo = np.append(horse_jokey_zisyo, row2[1]*1.0)
            horse_jokey_trainer_zisyo = np.append(horse_jokey_zisyo, row2[2]*1.0)
            win_rate_zisyo = np.append(win_rate, np.array([horse_jokey_trainer_zisyo]), axis=0)

    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        StopSSHSession(server, connection)
    connection.commit()
    StopSSHSession(server, connection)

    svM_test, svM_training = make_training(race_result, race_predata)

    #馬、騎手、調教師が関係する勝率を計算する
    hor, joc, tra = Num(win_rate_zisyo)

    arr3_copy = np.array(basic_wins_train_in)
    
    #勝率辞書から必要な（馬・騎手・調教師）情報を抜き取る
    print(basic_wins_in)
    testBasicWins, trainBasicWins = createWinsRate(basic_wins_in, basic_wins_train_in, hor, joc, tra)
    #前項の抜きとった値から出場馬の勝率を計算
    finBasicWins = raceBasicWinrate(trainBasicWins,arr3_copy)
    basicwins = dict(finBasicWins)
    print(finBasicWins)
    print("-----------------------")
    print(basicwins)


    #ここからSVMゾーン
    svmResult = Svm(race_result,race_predata)

    print(np.hstack((horseNameID.reshape(len(horseNameID),1),svmResult.reshape(len(svmResult),1))))
    svmResult_seikei = np.hstack((horseNameID.reshape(len(horseNameID),1),svmResult.reshape(len(svmResult),1)))

    #結果を出力
    f = open('20171125_kyoto3_ask.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')

    #福田メソッド
    for i in sorted(list(svmResult_seikei),key=lambda i:i[1]):
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
    for i in Aska_method(sorted(list(svmResult_seikei),key=lambda i:i[1])):
        a = sql_horce_name(str(i[0]).encode("utf-8").replace(".0", ""))
        writer.writerow(str(i[0])+":"+str(i[1])+":"+str(i[2]).replace(',', ''))
    """
    # ファイルクローズ
    f.close()

    print("finish")