# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import csv
import MySQLdb
import MySQLdb.cursors
import sql_horse_name
from sshtunnel import SSHTunnelForwarder
from time import sleep
from basic_wins import Num
#from basic_wins import createWinsRate
#from basic_wins import raceBasicWinrate
from basic_wins import normalize
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

def Aska_method(sumResult):
	raceResult = np.empty((0,3), float)

	for result in sumResult:
		umaResult = np.array([])
		key = str(sumResult[0])
		key = key.replace(".0", "")
		try:
			result = np.append(result, sumResult[0])
			result = np.append(result, sumResult[1])
			result = np.append(result, Aska(key))
		except:
			result = np.append(result, 0.0)
			print("errors")
		print(len(result))
		raceResult = np.append(raceResult, np.array([result]), axis = 0)

	return finResult
#SVMに使うデータを正規化する
def svm_make_training(test, training):
	
	if max(test[:,0]) >= max(training[:,1]):
		maxHorceYear = max(test[:,0])
	else:
		maxHorceYear = max(training[:,1])

	if max(test[:,1]) >= max(training[:,2]):
		maxHorceWeight = max(test[:,1])
	else:
		maxHorceWeight = max(training[:,2])

	if max(test[:,2]) >= max(training[:,3]):
		maxHorcePopularity = max(test[:,2])
	else:
		maxHorcePopularity = max(training[:,3])

	for predata in test:
		predata[0] = (predata[0]) / (maxHorceYear)
		predata[1] = (predata[1]) / (maxHorceWeight)
		predata[2] = (predata[2]) / (maxHorcePopularity)

	for result in training:
		result[1] = (result[1]) / (maxHorceYear)
		result[2] = (result[2]) / (maxHorceWeight)
		result[3] = (result[3]) / (maxHorcePopularity)

	return test, training

if __name__ == "__main__":
	
	sqlhorse_jokey_zisyolection = SQLCollection.SQLCollection()
	#学習用データセット作成
	SVMTrainData = sqlhorse_jokey_zisyolection.getTrainData()
	print(SVMTrainData)
		#if(SVMTrainData==-1):
		#return 0
	
	#上位3位の馬と騎手のデータ
	Top3HorseAndJockeyData = sqlhorse_jokey_zisyolection.getTop3HorseAndJockey()
		#if Top3HorseAndJockeyData ==-1:
		#return 0

	#テスト用データセット作成
	SVMTestData = sqlhorse_jokey_zisyolection.getTestData()
	print(SVMTestData)
		#if( SVMTestData ==-1):
		#return 0
	try:
		"""
		SVMTrainData = cursor.fetchall()
		selectWinRate = cursor.fetchall()
		
		SVMTestData = cursor.fetchall()
		"""
		horseNameID= np.array([])
		url = np.array([])
		
		race_predata = np.empty((0,3), float)
		basic_wins_test_in = np.empty((0,4), float)
		
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

			basic_wins_test_in = np.append(basic_wins_test_in, np.array([top3_horce_jokey]), axis=0)
			race_predata = np.append(race_predata, np.array([svm_test]), axis=0)

		race_result  = np.empty((0,4), float)
		basic_wins_train_in   = np.empty((0,4), float)
		
		#トレーニングデータをSVM用とbasic_wins用に格納
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
				basic_wins_train_in = np.append(basic_wins_train_in, np.array([top3_horce_jokey_trainning]), axis=0)

		win_rate_zisyo = np.empty((0,3), float)

		#basic_wins用の辞書作成
		for row2 in Top3HorseAndJockeyData:
			horse_jokey_trainer_zisyo = np.array([])
			horse_jokey_trainer_zisyo = np.append(horse_jokey_trainer_zisyo, row2[0]*1.0)
			horse_jokey_trainer_zisyo = np.append(horse_jokey_trainer_zisyo, row2[1]*1.0)
			horse_jokey_trainer_zisyo = np.append(horse_jokey_trainer_zisyo, row2[2]*1.0)
			win_rate_zisyo = np.append(win_rate_zisyo, np.array([horse_jokey_trainer_zisyo]), axis=0)

	except MySQLdb.Error as e:
		print('MySQLdb.Error: ', e)
		StopSSHSession(server, connection)
		connection.commit()
		StopSSHSession(server, connection)

	svM_test, svM_training = svm_make_training(race_predata, race_result)

	#馬、騎手、調教師が関係する勝率を計算する
	finBasicWins = Num(win_rate_zisyo,basic_wins_test_in, basic_wins_train_in)
	"""
	#勝率辞書から必要な（馬・騎手・調教師）情報を抜き取る
	testBasicWins, trainBasicWins = createWinsRate(basic_wins_in, basic_wins_train_in, hor, joc, tra)
	#前項の抜きとった値から出場馬の勝率を計算
	finBasicWins = raceBasicWinrate(trainBasicWins,arr3_copy)
	"""
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

	raceResult = np.empty((0,3), float)
	#福田メソッド
	for i in sorted(list(svmResult_seikei),key=lambda i:i[1]):
		umaResult = np.array([])
		try:
			print(i[0])
			print(basicwins[i[0]])
			umaResult = np.append(umaResult, i[0])
			umaResult = np.append(umaResult, i[1])
			umaResult = np.append(umaResult, basicwins[i[0]])
			writer.writerow(str(i[0])+":"+str(i[1])+":"+str(basicwins[i[0]]).replace(',', ''))
		except:
			umaResult = np.append(umaResult, i[0])
			umaResult = np.append(umaResult, i[1])
			umaResult = np.append(umaResult, 0.0)
			print("errors")
			writer.writerow(str(i[0])+":"+str(i[1])+":"+str(0.0).replace(',', ''))
		raceResult = np.append(raceResult, np.array([umaResult]), axis = 0)
	print(raceResult)
	
	#あすかメソッド
	"""
	for i in Aska_method(sorted(list(svmResult_seikei),key=lambda i:i[1])):
		a = sql_horce_name(str(i[0]).encode("utf-8").replace(".0", ""))
		writer.writerow(str(i[0])+":"+str(i[1])+":"+str(i[2]).replace(',', ''))
	"""
	# ファイルクローズ
	f.close()

	print("finish")