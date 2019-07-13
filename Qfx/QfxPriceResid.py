# coding=utf-8
import datetime
import numpy as np
import pandas as pd
from Qfx import QfxMySql, QfxPriceConfig


# **********************************************************
# QfxPriceResid
# **********************************************************
class QfxPriceResid:
	# ==========================================================
	# コンストラクタ
	# ----------------------------------------------------------
	# 引数
	# 	qfx_mysql:			MySQL データベースコントローラ
	# 	qfx_price_config:	価格情報設定
	# ==========================================================
	def __init__(
			self,
			qfx_mysql:			QfxMySql.QfxMySql,
			qfx_price_config:	QfxPriceConfig.QfxPriceConfig):
		self.m_qfxMySql: QfxMySql.QfxMySql = qfx_mysql								# MySQL データベースコントローラ
		self.m_qfxPriceConfig: QfxPriceConfig.QfxPriceConfig = qfx_price_config		# 価格情報設定

	# ==========================================================
	# 先頭シフトの日時を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	左端シフト日時と右端シフト日時、算定シフト日時を返します。
	# ==========================================================
	def get_time_first(self) -> tuple:
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_resid_shift_time_first.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																	# SQL 文を取得
		str_sql = str_sql.format(																	# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,												# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,										# 時間足
			nSamples=self.m_qfxPriceConfig.nSamples,												# サンプリング数
			nFrequency=self.m_qfxPriceConfig.nFrequency)											# 頻度
		df_result: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)						# 結果セットを取得
		dt_shift_left: datetime.datetime = None														# 左端シフト日時格納バッファを初期化
		dt_shift_right: datetime.datetime = None													# 右端シフト日時格納バッファを初期化
		dt_shift: datetime.datetime = None															# 算定シフト日時格納バッファを初期化
		if df_result.shape[0] == 1:																	# 結果セットが空でないなら・・・
			dt_shift_left = df_result.at[0, "shift_time_left"]										# 左端シフト日時を取得
			dt_shift_right = df_result.at[0, "shift_time_right"]									# 右端シフト日時を取得
			dt_shift = df_result.at[0, "shift_time"]												# 算定シフト日時を取得
		return dt_shift_left, dt_shift_right, dt_shift												# 戻り値

	# ==========================================================
	# 末尾シフトの日時を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_last(self) -> tuple:
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_resid_shift_time_last.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																	# SQL 文を取得
		str_sql = str_sql.format(																	# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,												# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,										# 時間足
			nSamples=self.m_qfxPriceConfig.nSamples,												# サンプリング数
			nFrequency=self.m_qfxPriceConfig.nFrequency)											# 頻度
		df_result: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)						# 結果セットを取得
		dt_shift_left: datetime.datetime = None														# 左端シフト日時格納バッファを初期化
		dt_shift_right: datetime.datetime = None													# 右端シフト日時格納バッファを初期化
		dt_shift: datetime.datetime = None															# 算定シフト日時格納バッファを初期化
		if df_result.shape[0] == 1:																	# 結果セットが空でないなら・・・
			dt_shift_left = df_result.at[0, "shift_time_left"]										# 左端シフト日時を取得
			dt_shift_right = df_result.at[0, "shift_time_right"]									# 右端シフト日時を取得
			dt_shift = df_result.at[0, "shift_time"]												# 算定シフト日時を取得
		return dt_shift_left, dt_shift_right, dt_shift												# 戻り値

	# ==========================================================
	# データソースをロード
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:	左端シフト日時
	# 	str_operator:	比較演算子
	# 	dt_shift_right:	右端シフト日時
	# ----------------------------------------------------------
	# 戻り値
	#   データソースを返します。
	# ==========================================================
	def load_source(
			self,
			dt_shift_left:	datetime.datetime,
			str_operator:	str,
			dt_shift_right:	datetime.datetime) -> pd.core.frame.DataFrame:
		str_shift_time_left: str = dt_shift_left.strftime('%Y-%m-%d %H:%M:%S')			# 左端シフト日時を文字列に変換
		str_shift_time_right: str = dt_shift_right.strftime('%Y-%m-%d %H:%M:%S')		# 右端シフト日時を文字列に変換
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_resid_value.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]														# SQL 文を取得
		str_sql = str_sql.format(														# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,									# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,							# 時間足
			nSamples=self.m_qfxPriceConfig.nSamples,									# サンプリング数
			nFrequency=self.m_qfxPriceConfig.nFrequency,								# 頻度
			strShiftTimeLeft=str_shift_time_left,										# 左端シフト日時
			strOperator=str_operator,													# 比較演算子
			strShiftTimeRight=str_shift_time_right)										# 右端シフト日時
		df: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)				# クエリを発行
		df.shift_time = pd.to_datetime(df.shift_time)									# "shift_time" を datetime64(Timestamp)型に変換
		df = df.set_index("shift_time")													# インデックス列を "shift_time" 列に指定
		dt_index: list[datetime.datetime] =\
			pd.date_range(dt_shift_left, end=dt_shift_right, freq="H")					# 開始日時から終了日時までの一時間ごとの日時を生成
		df = df.reindex(dt_index)														# 欠落している土日の日時をインデックスに含める
		df.close = df.value.astype(np.float64)											# 終値を float64 型に変換
		return df																		# 戻り値

	# ==========================================================
	# レコードを削除
	# ----------------------------------------------------------
	# 引数
	#   dt_shift_left:  左端シフト日時
	#   dt_shift_right: 右端シフト日時
	#   dt_shift:       算定シフト日時
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は False を返します。
	# ==========================================================
	def delete(
			self,
			dt_shift_left:	datetime.datetime,
			dt_shift_right:	datetime.datetime,
			dt_shift:		datetime.datetime) -> bool:
		str_shift_time_left: str = dt_shift_left.strftime('%Y-%m-%d %H:%M:%S')				# 左端シフト日時を文字列に変換
		str_shift_time_right: str = dt_shift_right.strftime('%Y-%m-%d %H:%M:%S')			# 右端シフト日時を文字列に変換
		str_shift_time: str = dt_shift.strftime('%Y-%m-%d %H:%M:%S')						# 算定シフト日時を文字列に変換
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_resid_delete.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]															# SQL 文を取得
		str_sql = str_sql.format(															# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,										# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,								# 時間足
			nSamples=self.m_qfxPriceConfig.nSamples,										# サンプリング数
			nFrequency=self.m_qfxPriceConfig.nFrequency,									# 頻度
			strShiftTimeLeft=str_shift_time_left,											# 左端シフト日時
			strShiftTimeRight=str_shift_time_right,											# 右端シフト日時
			strShiftTime=str_shift_time)													# 算定シフト日時
		if not self.m_qfxMySql.execute(str_sql):											# SQL 文を発行・・・
			return False																	# 処理中断
		return True																			# 戻り値

	# ==========================================================
	# レコードをすべて削除
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は False を返します。
	# ==========================================================
	def delete_all(self) -> bool:
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_resid_delete_all.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																# SQL 文を取得
		str_sql = str_sql.format(																# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,											# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,									# 時間足
			nSamples=self.m_qfxPriceConfig.nSamples,											# サンプリング数
			nFrequency=self.m_qfxPriceConfig.nFrequency)										# 頻度
		if not self.m_qfxMySql.execute(str_sql):												# SQL 文を発行・・・
			return False																		# 処理中断
		return True																				# 戻り値

	# ==========================================================
	# レコードを挿入
	# ----------------------------------------------------------
	# 引数
	#   dt_shift_left:  左端シフト日時
	#   dt_shift_right: 右端シフト日時
	#   dt_shift:       算定シフト日時
	#   f_value:        値
	# ----------------------------------------------------------
	# 戻り値
	#   処理が成功した場合は True を返します。それ以外の場合は
	#   False を返します。
	# ==========================================================
	def insert(
			self,
			dt_shift_left:	datetime.datetime,
			dt_shift_right:	datetime.datetime,
			dt_shift:		datetime.datetime,
			f_value:		float) -> bool:
		str_shift_time_left: str = dt_shift_left.strftime('%Y-%m-%d %H:%M:%S')				# 左端シフト日時を文字列に変換
		str_shift_time_right: str = dt_shift_right.strftime('%Y-%m-%d %H:%M:%S')			# 右端シフト日時を文字列に変換
		str_shift_time: str = dt_shift.strftime('%Y-%m-%d %H:%M:%S')						# 算定シフト日時を文字列に変換
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_resid_insert.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]															# SQL 文を取得
		str_sql = str_sql.format(															# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,										# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,								# 時間足
			nSamples=self.m_qfxPriceConfig.nSamples,										# サンプリング数
			nFrequency=self.m_qfxPriceConfig.nFrequency,									# 頻度
			strShiftTimeLeft=str_shift_time_left,											# 左端シフト日時
			strShiftTimeRight=str_shift_time_right,											# 右端シフト日時
			strShiftTime=str_shift_time,													# 算定シフト日時
			fValue=f_value)																	# 値
		if not self.m_qfxMySql.execute(str_sql):											# SQL 文を発行・・・
			return False																	# 処理中断
		return True																			# 戻り値
