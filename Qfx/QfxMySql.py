# coding=utf-8
import dataclasses
import pandas.io.sql
import mysql.connector
import pkg_resources
import configparser
from terminaltables import AsciiTable


# **********************************************************
# QfxMySqlConfig
# **********************************************************
@dataclasses.dataclass
class QfxMySqlConfig:
	strHost:		str = ""		# ホスト名
	strUser:		str = ""		# ユーザ名
	strPassword:	str = ""		# パスワード
	strSslCa:		str = ""		# SSL 認証ファイル
	strUsePure:		str = ""		# Python 実装を使用するか
	strDatabase:	str = ""		# データベース

	# ==========================================================
	# Load settings
	# ==========================================================
	def load_config(self):
		byn_ini = pkg_resources.resource_string("Qfx", "Config/MySql.ini")		# ファイル内容をバイナリデータで取得
		str_ini = byn_ini.decode()												# バイナリデータを文字列に変換
		cp: configparser.ConfigParser = configparser.ConfigParser()				# パーサを生成
		cp.read_string(str_ini)													# 設定を読み込み
		str_section: str = "MySql"												# セクション名を指定
		self.strHost = cp.get(str_section, "strHost")							# ホスト名を取得
		self.strUser = cp.get(str_section, "strUser")							# ユーザ名
		self.strPassword = cp.get(str_section, "strPassword")					# パスワード
		self.strSslCa = cp.get(str_section, "strSslCa")							# SSL 認証ファイル
		self.strUsePure = cp.get(str_section, "strUsePure")						# Python 実装を使用するか
		self.strDatabase = cp.get(str_section, "strDatabase")					# データベース名

	# ==========================================================
	# print settings
	# ==========================================================
	def print(self):
		lst_table = [
			["Item", "Settings"],
			["Host", self.strHost],
			["User", self.strUser],
			["Password", self.strPassword],
			["SSL CA", self.strSslCa],
			["Use pure", self.strUsePure],
			["Database", self.strDatabase]
		]
		table = AsciiTable(lst_table)
		print(table.table)


# **********************************************************
# QfxMySql
# **********************************************************
class QfxMySql:
	# ==========================================================
	# コンストラクタ
	# ----------------------------------------------------------
	# 引数
	# 	qfx_mysql_config:	MySQL 接続設定
	# ==========================================================
	def __init__(self, qfx_mysql_config: QfxMySqlConfig):
		self.m_qfxMySqlConfig = qfx_mysql_config		# 接続設定を生成
		self.m_mysqlDb = None							# MySQL データベースコネクタ

	# ==========================================================
	# MySQL データベースに接続
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def connect(self) -> bool:
		b_ret = False											# 処理結果フラグを初期化
		try:													# 例外処理開始
			self.m_mysqlDb = mysql.connector.connect( 			# 接続
				host=self.m_qfxMySqlConfig.strHost,				# ホスト名
				user=self.m_qfxMySqlConfig.strUser,				# ユーザ名
				password=self.m_qfxMySqlConfig.strPassword,		# パスワード
				# ssl_ca=self.m_qfxMySqlConfig.strSslCa,			# SSL 認証権限
				# use_pure=self.m_qfxMySqlConfig.strUsePure,		# pure Python を使うか
				pool_name="mypool",
				pool_size=3,
				database=self.m_qfxMySqlConfig.strDatabase)		# データベース名
			b_ret = True										# 処理結果フラグを更新
		except mysql.connector.Error as mysqlError:				# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)					# 通知
		finally:												# 終了処理・・・
			return b_ret										# 戻り値

	# ==========================================================
	# MySQL データベースを切断
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def disconnect(self) -> bool:
		b_ret = False									# 処理結果フラグを初期化
		if self.m_mysqlDb is None:						# コネクタが未生成なら・・・
			return b_ret								# 処理中断
		try:											# 例外処理開始
			self.m_mysqlDb.close()						# 切断
			b_ret = True								# 処理結果フラグを更新
		except mysql.connector.Error as mysqlError:		# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)			# 通知
		finally:										# 終了処理・・・
			return b_ret								# 戻り値

	# ==========================================================
	# MySQL データベースに接続中か調べる
	# ----------------------------------------------------------
	# 戻り値
	#   MySQL データベースに接続中の場合は True を返します。
	#   それ以外の場合は False を返します。
	# ==========================================================
	def is_connected(self) -> bool:
		if self.m_mysqlDb is None:					# コネクタが未生成なら・・・
			return False							# 処理中断
		return self.m_mysqlDb.is_connected()		# 切断

	# ==========================================================
	# MySQL データベースへの接続を維持する
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def ping(self) -> bool:
		b_ret = False									# 処理結果フラグを初期化
		if self.m_mysqlDb is None:						# コネクタが未生成なら・・・
			return b_ret								# 処理中断
		try:											# 例外処理開始
			self.m_mysqlDb.ping(reconnect=True)			# 切断されたら再接続
			b_ret = True								# 処理結果フラグを更新
		except mysql.connector.Error as mysqlError:		# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)			# 通知
		finally:										# 終了処理・・・
			return b_ret								# 戻り値

	# ==========================================================
	# SQL 文を発行
	# ----------------------------------------------------------
	# 引数
	#   str_sql:    SQL 文
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def execute(self, str_sql: str) -> bool:
		b_ret = False									# 処理結果フラグを初期化
		if self.m_mysqlDb is None:						# コネクタが未生成なら・・・
			return b_ret								# 処理中断
		cursor = self.m_mysqlDb.cursor()				# カーソルを取得
		try:											# ▽例外処理開始
			cursor.execute(str_sql)						# SQL 文を発行
			b_ret = True								# 処理結果フラグを更新
		except mysql.connector.Error as mysqlError:		# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)			# 通知
		finally:										# 終了処理・・・
			cursor.close()								# カーソルをクローズ
			return b_ret								# 戻り値

	# ==========================================================
	# コミット
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def commit(self) -> bool:
		b_ret = False									# 処理結果フラグを初期化
		if self.m_mysqlDb is None:						# コネクタが未生成なら・・・
			return b_ret								# 処理中断
		try:											# ▽例外処理開始
			self.m_mysqlDb.commit()						# コミット
			b_ret = True								# 処理結果フラグを更新
		except mysql.connector.Error as mysqlError:		# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)			# 通知
		finally:										# 終了処理・・・
			return b_ret								# 戻り値

	# ==========================================================
	# ロールバック
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def rollback(self) -> bool:
		b_ret = False									# 処理結果フラグを初期化
		if self.m_mysqlDb is None:						# コネクタが未生成なら・・・
			return b_ret								# 処理中断
		try:											# ▽例外処理開始
			self.m_mysqlDb.rollback()					# ロールバック
			b_ret = True								# 処理結果フラグを更新
		except mysql.connector.Error as mysqlError:		# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)			# 通知
		finally:										# 終了処理・・・
			return b_ret								# 戻り値

	# ==========================================================
	# クエリを発行
	# ----------------------------------------------------------
	# 引数
	#   str_sql:    SQL 文
	# ----------------------------------------------------------
	# 戻り値
	# 	データフレームを返します。
	# ==========================================================
	def fetch_all(self, str_sql: str) -> bool:
		try:															# ▽例外処理開始
			df = pandas.io.sql.read_sql(str_sql, self.m_mysqlDb)		# 結果セットを取得
		except mysql.connector.Error as mysqlError:						# 例外を捕捉・・・
			print("MySQL Error: ", mysqlError)							# 通知
		return df														# 戻り値

	# ==========================================================
	# SQL 文をファイルからロード
	# ----------------------------------------------------------
	# 引数
	#   str_file_path:	ファイルパス
	# ----------------------------------------------------------
	# 戻り値
	# 	SQL 文のリストを返します。
	# ==========================================================
	@staticmethod
	def get_sql(str_file_path: str) -> list:
		byn_contents = pkg_resources.resource_string('Qfx', str_file_path)		# ファイル内容をバイナリデータで取得
		str_contents = byn_contents.decode()									# バイナリデータを文字列に変換
		ary_sql = str_contents.split(';')										# SQL 文の配列を取得
		return ary_sql															# 戻り値
