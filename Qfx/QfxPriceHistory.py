# coding=utf-8
import datetime
import numpy as np
import pandas as pd
from Qfx import QfxMySql, QfxPriceConfig


# **********************************************************
# QfxPriceHistory
# **********************************************************
class QfxPriceHistory:
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
	# 最初の日時を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_first(self) -> datetime.datetime:
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_shift_time_first.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																		# SQL 文を取得
		str_sql = str_sql.format(																		# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,													# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames)											# 時間足
		df_result: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)							# 結果セットを取得
		dt_shift: datetime.datetime = None																# シフト日時格納バッファを初期化
		if df_result.shape[0] == 1:																		# 結果セットが空でないなら・・・
			dt_shift = df_result.at[0, "shift_time"]													# シフト日時を取得
		return dt_shift																					# 戻り値

	# ==========================================================
	# 最後の日時を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_last(self) -> datetime.datetime:
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_shift_time_last.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																	# SQL 文を取得
		str_sql = str_sql.format(																	# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,												# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames)										# 時間足
		df_result: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)						# 結果セットを取得
		dt_shift: datetime.datetime = None															# シフト日時格納バッファを初期化
		if df_result.shape[0] == 1:																	# 結果セットが空でないなら・・・
			dt_shift = df_result.at[0, "shift_time"]												# シフト日時を取得
		return dt_shift																				# 戻り値

	# ==========================================================
	# 指定シフト日時より後のシフト日時を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:	左端シフト日時
	# 	n_offset:		オフセット(0 は dt_shift_left に一致)
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_forward(self, dt_shift_left: datetime.datetime, n_offset: int) -> datetime.datetime:
		str_shift_left: str = dt_shift_left.strftime('%Y-%m-%d %H:%M:%S')								# 左端シフト日時を文字列に変換
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_shift_time_forward.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																		# SQL 文を取得
		str_sql = str_sql.format(																		# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,													# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,											# 時間足
			strShiftTime=str_shift_left,																# シフト日時
			nOffset=n_offset)																			# オフセット
		df_result: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)							# クエリを発行
		dt_shift: datetime.datetime = None																# シフト日時格納バッファを初期化
		if df_result.shape[0] == 1:																		# 結果セットが空でないなら・・・
			dt_shift = df_result.at[0, "shift_time"]													# シフト日時を取得
		return dt_shift																					# 戻り値

	# ==========================================================
	# 指定シフト日時より前のシフト日時を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_right:	右端シフト日時
	# 	n_offset:		オフセット(0 は dt_shift_right に一致)
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_backward(self, dt_shift_right: datetime.datetime, n_offset: int) -> datetime.datetime:
		str_shift_right: str = dt_shift_right.strftime('%Y-%m-%d %H:%M:%S')								# 右端シフト日時を文字列に変換
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_shift_time_backward.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]																		# SQL 文を取得
		str_sql = str_sql.format(																		# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,													# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,											# 時間足
			strShiftTime=str_shift_right,																# シフト日時
			nOffset=n_offset)																			# オフセット
		df_result: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)							# クエリを発行
		dt_shift: datetime.datetime = None																# シフト日時格納バッファを初期化
		if df_result.shape[0] == 1:																		# 結果セットが空でないなら・・・
			dt_shift = df_result.at[0, "shift_time"]													# シフト日時を取得
		return dt_shift																					# 戻り値

	# ==========================================================
	# 指定シフト日時の直後のシフト日時を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:	左端シフト日時
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_next(self, dt_shift_left: datetime.datetime) -> datetime.datetime:
		dt_shift: datetime.datetime = self.get_time_forward(dt_shift_left, 1)		# 直後のシフト日時を取得
		return dt_shift																# 戻り値

	# ==========================================================
	# 指定シフト日時の直前のシフト日時を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_right:	右端シフト日時
	# ----------------------------------------------------------
	# 戻り値
	# 	シフト日時を返します。
	# ==========================================================
	def get_time_prev(self, dt_shift_right: datetime.datetime) -> datetime.datetime:
		dt_shift: datetime.datetime = self.get_time_backward(dt_shift_right, 1)		# 直前のシフト日時を取得
		return dt_shift																# 戻り値

	# ==========================================================
	# 期間を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:  左端シフト日時
	# 	n_samples:      サンプリング数
	# ----------------------------------------------------------
	# 戻り値
	# 	左端シフト日時と右端シフト日時を返します。
	# ==========================================================
	def get_time_range(
			self,
			dt_shift_left:	datetime.datetime,
			n_samples:		int) -> tuple:
		n_offset: int = n_samples - 1															# 左端シフト日時からのオフセット
		if dt_shift_left is None:																# 左端シフト日時が未指定なら
			dt_shift_left = self.get_time_first()												# 左端シフト日時を初期化
		dt_shift_right: datetime.datetime = self.get_time_forward(dt_shift_left, n_offset)		# 右端シフト日時を取得
		return dt_shift_left, dt_shift_right													# 戻り値

	# ==========================================================
	# 指定左端シフト日時のオフセット日時を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:	左端シフト日時
	# 	n_offset:		オフセット
	# ----------------------------------------------------------
	# 戻り値
	# 	右端シフト日時を返します。
	# ==========================================================
	def get_time_right(self, dt_shift_left: datetime.datetime, n_offset: int) -> datetime.datetime:
		if dt_shift_left is None:																# 左端シフト日時が未指定なら
			dt_shift_left = self.get_time_first()												# 左端シフト日時を初期化
		dt_shift_right: datetime.datetime = self.get_time_forward(dt_shift_left, n_offset)		# 右端シフト日時を取得
		return dt_shift_right																	# 戻り値

	# ==========================================================
	# 指定右端シフト日時のオフセット日時を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_right:	右端シフト日時
	# 	n_offset:		オフセット
	# ----------------------------------------------------------
	# 戻り値
	# 	左端シフト日時を返します。
	# ==========================================================
	def get_time_left(self, dt_shift_right: datetime.datetime, n_offset: int) -> datetime.datetime:
		if dt_shift_right is None:																# 右端シフト日時が未指定なら
			dt_shift_right = self.get_time_last()												# 右端シフト日時を初期化
		dt_shift_left: datetime.datetime = self.get_time_backward(dt_shift_right, n_offset)		# 左端シフト日時を取得
		return dt_shift_left																	# 戻り値

	# ==========================================================
	# レコード数を取得
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:	左端シフト日時
	# 	dt_shift_right:	右端シフト日時
	# ----------------------------------------------------------
	# 戻り値
	# 	レコード数を返します。
	# ==========================================================
	def count_source(
			self,
			dt_shift_left:	datetime.datetime,
			dt_shift_right:	datetime.datetime) -> int:
		str_shift_time_left: str = dt_shift_left.strftime('%Y-%m-%d %H:%M:%S')					# 左端シフト日時を文字列に変換
		str_shift_time_right: str = dt_shift_right.strftime('%Y-%m-%d %H:%M:%S')				# 右端シフト日時を文字列に変換
		lst_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_count.sql")			# SQL 文をロード
		str_sql: str = lst_sql[0]																# SQL 文を取得
		str_sql = str_sql.format(																# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,											# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,									# 時間足
			strShiftTimeLeft=str_shift_time_left,												# 左端シフト日時
			strShiftTimeRight=str_shift_time_right)												# 右端シフト日時
		df: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)						# クエリを発行
		n_count = df.iat[0, 0]																	# レコード数を取得
		return n_count																			# 戻り値

	# ==========================================================
	# データソースをロード
	# ----------------------------------------------------------
	# 引数
	# 	dt_shift_left:	左端シフト日時
	# 	str_operator:	比較演算子
	# 	dt_shift_right:	右端シフト日時
	# ----------------------------------------------------------
	# 戻り値
	# 	データソースを返します。
	# ==========================================================
	def load_source(
			self,
			dt_shift_left:	datetime.datetime,
			str_operator:	str,
			dt_shift_right:	datetime.datetime) -> pd.core.frame.DataFrame:
		str_shift_time_left: str = dt_shift_left.strftime('%Y-%m-%d %H:%M:%S')				# 左端シフト日時を文字列に変換
		str_shift_time_right: str = dt_shift_right.strftime('%Y-%m-%d %H:%M:%S')			# 右端シフト日時を文字列に変換
		ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_close.sql")		# SQL 文をロード
		str_sql: str = ary_sql[0]															# SQL 文を取得
		str_sql = str_sql.format(															# SQL 文を構成
			strSymbol=self.m_qfxPriceConfig.strSymbol,										# 銘柄名
			strTimeFrames=self.m_qfxPriceConfig.strTimeFrames,								# 時間足
			strShiftTimeLeft=str_shift_time_left,											# 左端シフト日時
			strOperator=str_operator,														# 比較演算子
			strShiftTimeRight=str_shift_time_right)											# 右端シフト日時
		df: pd.core.frame.DataFrame = self.m_qfxMySql.fetch_all(str_sql)					# クエリを発行
		df.shift_time = pd.to_datetime(df.shift_time)										# "shift_time" を datetime64(Timestamp)型に変換
		df = df.set_index("shift_time")														# インデックス列を "shift_time" 列に指定
		dt_index: list[datetime.datetime] = \
			pd.date_range(dt_shift_left, end=dt_shift_right, freq="H")						# 開始日時から終了日時までの一時間ごとの日時を生成
		df = df.reindex(dt_index)															# 欠落している土日の日時をインデックスに含める
		df.close = df.close.astype(np.float64)												# 終値を float64 型に変換
		return df																			# 戻り値
