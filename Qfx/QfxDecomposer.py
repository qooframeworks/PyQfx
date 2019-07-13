# coding=utf-8
import datetime
import pandas as pd
import statsmodels
import statsmodels.api as sm
from Qfx import QfxCommon, QfxMySql, QfxPriceConfig, QfxPriceSeasonal, QfxPriceHistory, QfxPriceTrend, QfxPriceResid


# **********************************************************
# QfxDecomposer
# **********************************************************
class QfxDecomposer:
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
		self.m_qfxPriceHistory = QfxPriceHistory.QfxPriceHistory(					# 価格履歴を生成
			self.m_qfxMySql,														# MySQL データベースコントローラ
			self.m_qfxPriceConfig)													# 価格情報設定
		self.m_qfxPriceTrend = QfxPriceTrend.QfxPriceTrend(							# トレンドを生成
			self.m_qfxMySql,														# MySQL データベースコントローラ
			self.m_qfxPriceConfig)													# 価格情報設定
		self.m_qfxPriceSeasonal = QfxPriceSeasonal.QfxPriceSeasonal(				# 季節性周期を生成
			self.m_qfxMySql,														# MySQL データベースコントローラ
			self.m_qfxPriceConfig)													# 価格情報設定
		self.m_qfxPriceResid = QfxPriceResid.QfxPriceResid(							# 残差を生成
			self.m_qfxMySql,														# MySQL データベースコントローラ
			self.m_qfxPriceConfig)													# 価格情報設定

	# ==========================================================
	# 周期計算のサンプリング範囲を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	開始シフト日時と終了シフト日時を返します。
	# ==========================================================
	def get_sampling_range(self) -> tuple:
		dt_shift_left: datetime.datetime = None																	# 左端シフト日時を初期化
		dt_shift_right: datetime.datetime = None																# 右端シフト日時を初期化
		dt_trend_shift_left, dt_trend_shift_right, dt_trend_shift = self.m_qfxPriceTrend.get_time_last()		# 末尾トレンドの集計日時を取得
		if dt_trend_shift_left is None:																			# トレンドを未出力なら・・・
			dt_shift_left = self.m_qfxPriceHistory.get_time_first()												# 左端シフト日時を構成
		else:																									# トレンドを未出力でないなら・・・
			dt_shift_left = self.m_qfxPriceHistory.get_time_next(dt_trend_shift_left)							# 左端シフト日時を構成
		if dt_shift_left is None:																				# 左端シフト日時が見つからないなら・・・
			print("There is not history to analyze.")															# 通知
			return dt_shift_left, dt_shift_right																# 処理中断
		n_offset: int = self.m_qfxPriceConfig.nSamples - 1														# オフセットを構成
		dt_shift_right = self.m_qfxPriceHistory.get_time_right(dt_shift_left, n_offset)							# 右端シフト日時を取得
		if dt_shift_right is None:																				# 右端シフト日時が有効範囲外なら・・・
			print("There is not history to analyze.")															# 通知
		return dt_shift_left, dt_shift_right																	# 処理中断

	# ==========================================================
	# 周期解析対象の範囲を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	開始シフト日時と終了シフト日時を返します。
	# ==========================================================
	def get_analysis_object_range(self) -> tuple:
		dt_shift_left: datetime.datetime = None																	# 左端シフト日時を初期化
		dt_shift_right: datetime.datetime = None																# 右端シフト日時を初期化
		dt_trend_shift_left, dt_trend_shift_right, dt_trend_shift = self.m_qfxPriceTrend.get_time_last()		# 末尾トレンドの集計日時を取得
		if dt_trend_shift_left is None:																			# トレンドを未出力なら・・・
			dt_shift_left = self.m_qfxPriceHistory.get_time_first()												# 左端シフト日時を構成
		else:																									# トレンドを未出力でないなら・・・
			dt_shift_left = self.m_qfxPriceHistory.get_time_next(dt_trend_shift_left)							# 左端シフト日時を構成
		if dt_shift_left is None:																				# 左端シフト日時が見つからないなら・・・
			print("There is not history to analyze.")															# 通知
			return dt_shift_left, dt_shift_right																# 処理中断
		dt_shift_right = self.m_qfxPriceHistory.get_time_last()													# 右端シフト日時を取得
		if dt_shift_right is None:																				# 右端シフト日時が有効範囲外なら・・・
			print("There is not history to analyze.")															# 通知
		return dt_shift_left, dt_shift_right																	# 処理中断

	# ==========================================================
	# 周期解析回数を取得
	# ----------------------------------------------------------
	# 戻り値
	# 	周期解析回数を返します。
	# ==========================================================
	def get_analysis_times(self) -> int:
		dt_shift_left, dt_shift_right = self.get_analysis_object_range()						# 周期解析対象の範囲を取得
		if dt_shift_left is None or dt_shift_right is None:										# 周期計算対象がないなら・・・
			return 0																			# 処理中断
		n_bars: int = self.m_qfxPriceHistory.count_source(dt_shift_left, dt_shift_right)		# 価格履歴の数を取得
		n_times: int = n_bars - (self.m_qfxPriceConfig.nSamples - 1)							# 周期計算回数を初期化
		if n_times < 1:																			# 周期解析対象数がサンプリング数未満なら・・・
			return 0																			# 処理中断
		return n_times																			# 戻り値

	# ==========================================================
	# 周期解析結果をクリア
	# ----------------------------------------------------------
	# 戻り値
	# 	処理が成功した場合は True を返します。それ以外の場合は False を返します。
	# ==========================================================
	def clear_analysis(self) -> bool:
		if not self.m_qfxPriceTrend.delete_all():           # トレンドを削除・・・
			print("failed to delete_all price_trend")       # 通知
			return False                                    # 処理中断
		if not self.m_qfxPriceSeasonal.delete_all():        # 季節性周期を削除・・・
			print("failed to delete_all price_seasonal")    # 通知
			return False                                    # 処理中断
		if not self.m_qfxPriceResid.delete_all():           # 残差を削除・・・
			print("failed to delete_all price_resid")       # 通知
			return False                                    # 処理中断
		return True                                         # 戻り値

	# ==========================================================
	# 周期を計算
	# ----------------------------------------------------------
	# 戻り値
	# 	処理が成功した場合は True を返します。それ以外の場合は False を返します。
	# ==========================================================
	def analyze(self) -> bool:
		dt_shift_left, dt_shift_right = self.get_sampling_range()							# 周期計算のサンプリング範囲を取得
		if dt_shift_left is None or dt_shift_right is None:									# 周期計算対象がないなら・・・
			print("dt_shift_left=%s, dt_shift_right=%s" % (QfxCommon.dt_to_str(dt_shift_left), QfxCommon.dt_to_str(dt_shift_right)))
			return False																	# 処理中断
		df_price_history: pd.core.frame.DataFrame = self.m_qfxPriceHistory.load_source(
			dt_shift_left, "<=", dt_shift_right)											# 指定範囲の価格履歴を抽出
		dr: statsmodels.tsa.seasonal.DecomposeResult = sm.tsa.seasonal_decompose(
			df_price_history.dropna(), freq=self.m_qfxPriceConfig.nFrequency)				# 周期分解
		df_trend: pd.core.frame.DataFrame = dr.trend.dropna().tail(1)						# トレンドを取得
		df_seasonal: pd.core.frame.DataFrame = dr.seasonal.dropna().tail(1)					# 季節性を取得
		df_resid: pd.core.frame.DataFrame = dr.resid.dropna().tail(1)						# 残差を取得
		if not self.m_qfxPriceTrend.insert(													# トレンドを出力
				dt_shift_left,																# 左端シフト日時
				dt_shift_right,																# 右端シフト日時
				df_trend.index[0],															# 算定シフト日時
				df_trend.iat[0, 0]):														# 値
			return False																	# 処理中断
		if not self.m_qfxPriceSeasonal.insert(												# 季節性周期を出力
				dt_shift_left,																# 左端シフト日時
				dt_shift_right,																# 右端シフト日時
				df_seasonal.index[0],														# 算定シフト日時
				df_seasonal.iat[0, 0]):														# 値
			return False																	# 処理中断
		if not self.m_qfxPriceResid.insert(													# 残差を出力
				dt_shift_left,																# 左端シフト日時
				dt_shift_right,																# 右端シフト日時
				df_resid.index[0],															# 算定シフト日時
				df_resid.iat[0, 0]):														# 値
			return False																	# 処理中断
		return True																			# 戻り値
