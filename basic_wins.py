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

def Num(win_rate_zisyo, test, train):
	#馬と騎手と調教師の勝率をそれぞれの配列に分け計算する。
	#createWinsRate,raceBasicWinrate組み合わせ
	horse, jokey, trainer = np.hsplit(win_rate_zisyo, [1,2])
	horse2= np.ravel(horse.T)
	jokey2= np.ravel(jokey.T)
	trainer2 = np.ravel(trainer.T)
	
	horse_zisyo = np.empty((0,2), float)
	jokey_zisyo = np.empty((0,2), float)
	trainer_zisyo = np.empty((0,2),float)
	
	for horseElement in horse2:
		zisyo =  np.array([])
		zisyo = np.append(zisyo, horseElement)
		zisyo = np.append(zisyo, (len(np.where(horse2==horseElement)[0])*1.0) / (len(win_rate_zisyo)*1.0))
		horse_zisyo = np.append(horse_zisyo, np.array([zisyo]), axis=0)
	for jockeyElement in jokey2:
		zisyo2 =  np.array([])
		zisyo2 = np.append(zisyo2, jockeyElement)
		zisyo2 = np.append(zisyo2, (len(np.where(jokey2==jockeyElement)[0])*1.0) / (len(win_rate_zisyo)*1.0))
		jokey_zisyo = np.append(jokey_zisyo, np.array([zisyo2]), axis=0)
	for trainerElement in trainer2:
		zisyo3 =  np.array([])
		zisyo3 = np.append(zisyo3, jokey_zisyo)
		zisyo3 = np.append(zisyo3, (len(np.where(trainer2==jokey_zisyo)[0])*1.0) / (len(win_rate_zisyo)*1.0))
		trainer_zisyo = np.append(trainer_zisyo, np.array([zisyo3]), axis=0)
	#各要素(馬の勝率、騎手の勝率、調教師の勝率を正規化)
	nrHorse_zisyo = normalize(horse_zisyo)
	nrJokey_zisyo = normalize(jokey_zisyo)
	nrTrainer_zisyo = normalize(trainer_zisyo)

	train_result = np.empty((0,2), float)
	for result in train:
		wkTrainResult =np.empty((0,2), float)
		wkTrainResult = np.append(wkTrainResult, result[0])
		horse_zisyo_train = list(np.where(horse_zisyo[:,0]==result[1]))
		jockey_zisyo_train = list(np.where(jockey_zisyo[:,0]==result[2]))
		trainer_train = list(np.where(trainer_zisyo[:,0]==result[3]))
			
		if len(list(horse_zisyo_train[0])) == 0:
			result[1] = 0.0
		else:
			for io in list(horse_zisyo_train[0]):
				result[1] = horse_zisyo[int(io)][1]
			
		if len(list(jockey_zisyo_train[0])) == 0:
			result[2] = 0.0
		else:
			for ip in list(jockey_zisyo_train[0]):
				result[2] = jockey_zisyo[int(ip)][1]

		if len(list(trainer_train[0])) == 0:
			result[3] = 0.0
		else:
			for iq in list(trainer_train[0]):
				result[3] = trainer[int(iq)][1]
		wkTrainResult = np.append(wkTrainResult, result[1]+result[2]+result[3])
		train_result = np.append(train_result, np.array([wkTrainResult]), axis = 0)
	return train_result

def normalize(targetArray):
	for targetElement in targetArray:
		targetElement[1] =max(targetArray[:,1])
	return targetArray



"""

def createWinsRate(test, train, horse, jockey, trainer):
	#辞書からテストデータとトレーニングデータの勝率を引っ張る
	for predata in test:
		horse_test   = list(np.where(horse[:,0]==predata[1]))
		jockey_test  = list(np.where(jockey[:,0]==predata[2]))
		trainer_test = list(np.where(jockey[:,0]==predata[3]))
		for io in list(horse_test[0]):
			predata[1] = horse[int(io)][1]
		for ip in list(jockey_test[0]):
			predata[2] = jockey[int(ip)][1]
		for iq in list(trainer_test[0]):
			predata[3] = trainer[int(iq)][1]

	for result in train:
		
		horse_train = list(np.where(horse[:,0]==result[1]))
		jockey_train = list(np.where(jockey[:,0]==result[2]))
		trainer_train = list(np.where(trainer[:,0]==result[3]))
		
		if len(list(horse_train[0])) == 0:
			result[1] = 0.0
		else:
			for io in list(horse_train[0]):
				result[1] = horse[int(io)][1]
		
		if len(list(jockey_train[0])) == 0:
			result[2] = 0.0
		else:
			for ip in list(jockey_train[0]):
				result[2] = jockey[int(ip)][1]
		
		if len(list(trainer_train[0])) == 0:
			result[3] = 0.0
		else:
			for iq in list(trainer_train[0]):
				result[3] = trainer[int(iq)][1]

	return test, train

#各勝率を足し合わせる
def raceBasicWinrate(arr3,arr_before):
	finBasicWins = np.empty((0,2), float)
	for ara, iou in zip(arr3, arr_before):
		raceZisyo = np.array([])
		sumRate = ara[1]+ara[2]+ara[3]
		raceZisyo = np.append(ccc, iou[1])
		raceZisyo = np.append(ccc, sumRate)
		finBasicWins = np.append(finBasicWins, np.array([raceZisyo]), axis=0)
	return np.array(sorted(list(finBasicWins),key=lambda i:i[1]))
"""
