# -*- coding: utf-8 -*-
from sshtunnel import SSHTunnelForwarder
import MySQLdb

class SQLCollection:
	
	def __init__(self):
		self.address = "yuruhuwa-bourg.sakura.ne.jp"
		self.user = "yuruhuwa-bourg"
		self.passwd = "eh4uat56gu"

		self.server = self.startSSHSession()
		self.connection = self.getConnection(self.server.local_bind_port)
		self.cursor = self.connection.cursor()


	def startSSHSession(self):
		server = SSHTunnelForwarder(
								(self.address, 22),
								ssh_username=self.user,
								ssh_password=self.passwd,
								remote_bind_address=('mysql541.db.sakura.ne.jp', 3306)
								)
		server.start()
		return server


	def getConnection(self, port):
		connection = MySQLdb.connect(
									 host='127.0.0.1',
									 port=port,
									 user='yuruhuwa-bourg', 
									 passwd='1q2w3e4r', 
									 db='yuruhuwa-bourg_keiba', 
									 charset='utf8')
		return connection

	def stopSSHSession(self, server, connection):
		connection.close()
		server.stop()

	def getTrainData(self):
		#学習用データセット作成
		sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, tkd.basis_weight, tkd.trainer_id, tkd.popularity, tkd.url "
		sql += "FROM t_keiba_data_result AS tkd "
		sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
		sql +=	"LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id "
		sql +=	"LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"

		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except MySQLdb.Error as e:
			self.stopSSHSession()
			return -1

	def getTop3HorseAndJockey(self):
		#学習用データセット作成
		sql2 = "SELECT tkd.horse_name_id, tkd.jockey_id, tkd.trainer_id "
		sql2 += "FROM t_keiba_data_result AS tkd"
		sql2 +=	" LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
		sql2 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id "
		sql2 +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
		sql2 +=	" WHERE tkd.score = 1"

		try:
			self.cursor.execute(sql2)
			return self.cursor.fetchall()
		except MySQLdb.Error as e:
			self.stopSSHSession()
			return -1

	def getTestData(self):
		sql3 = "SELECT tkd.id, tkd.horse_name_id, tkd.jockey_id,tkd.horse_sex, tkd.horse_year, tkd.basis_weight, tkd.url, tkd.trainer_id, tkd.popularity "
		sql3 += "FROM t_keiba_predata AS tkd "
		sql3 +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
		sql3 +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
		sql3 +=	"	LEFT JOIN m_trainer as mk ON tkd.trainer_id = mk.trainer_id"
		sql3 +=	"   WHERE tkd.url = 201705050811"

		try:
			self.cursor.execute(sql3)
			return self.cursor.fetchall()
		except MySQLdb.Error as e:
			self.stopSSHSession()
			return -1






			
