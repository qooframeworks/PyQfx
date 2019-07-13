# coding=utf-8
import numpy as np
import pandas as pd
from terminaltables import AsciiTable
from tqdm import tqdm as tqdm
from Qfx import QfxCommon
from Qfx import QfxMySql
from Qfx import QfxDecomposer
from Qfx import QfxPriceConfig
from Qfx import QfxPriceHistory
from Qfx import QfxPriceResid
from Qfx import QfxPriceSeasonal
from Qfx import QfxPriceShiftTime
from Qfx import QfxPriceTrend

# **********************************************************
# Global variables
# **********************************************************
_n_samples: int = 24 * 20                                                   # Number of samples for each calculating
_n_frequency: int = 24 * 5                                                  # Cycle assumed
# (This time around, use number of bars per a week as _n_frequency)
_qfx_mysql_config: QfxMySql.QfxMySqlConfig = QfxMySql.QfxMySqlConfig()      # MySQL connection settings
_df_summary_price_history: pd.core.frame.DataFrame = None                   # Summary of price history


# **********************************************************
# Function
# **********************************************************

# ==========================================================
# Initialize configuration of MySQL
# ==========================================================
def init_mysql_config():
    _qfx_mysql_config.load_config()     # Load MySql connection settings


# ==========================================================
# Show MySql connection settings
# ==========================================================
def show_mysql_config():
    _qfx_mysql_config.print()


# ==========================================================
# Load summary totaling up number of bars by symbols and timeframes
# ----------------------------------------------------------
# Returns:
# 	a summary as dataframe
# ==========================================================
def load_summary_price_history() -> pd.core.frame.DataFrame:
    qfx_mysql: QfxMySql.QfxMySql = QfxMySql.QfxMySql(_qfx_mysql_config)                 # create connector for MySQL
    if not qfx_mysql.connect():                                                         # connect to MySQL...
        print("failed to connect MySQL.")                                               # notify error message
        return None                                                                     # suspend process
    ary_sql: list[str] = QfxMySql.QfxMySql.get_sql("Sql/price_history_total.sql")       # load SQL file
    str_sql: str = ary_sql[0]                                                           # get SQL sentence
    df: pd.core.frame.DataFrame = qfx_mysql.fetch_all(str_sql)                          # fetch result
    if not qfx_mysql.disconnect():                                                      # disconnect MySQL...
        print("failed to disconnect MySQL.")                                            # notiry error message
    return df                                                                           # return


# ==========================================================
# 周期解析器を生成
# ----------------------------------------------------------
# 引数
#   qfx_mysql:          MySQL コネクタ
#   str_symbol:         銘柄名(symbol name)
#   str_time_frames:    時間足(identifier of bar's period)
#   n_samples:          サンプリング数(number of samples)
#   n_frequency:        頻度
# ----------------------------------------------------------
# 戻り地
#   周期解析器を返します。
# ==========================================================
def create_decomposer(
        qfx_mysql:          QfxMySql.QfxMySql,
        str_symbol:         str,
        str_time_frames:    str,
        n_samples:          int,
        n_frequency:        int) -> QfxDecomposer.QfxDecomposer:
    qfx_price_config = QfxPriceConfig.QfxPriceConfig(str_symbol, str_time_frames, n_samples, n_frequency)   # 価格履歴設定を構成
    qfx_decomposer = QfxDecomposer.QfxDecomposer(qfx_mysql, qfx_price_config)                               # 周期解析器を構成
    return qfx_decomposer                                                                                   # 戻り地


# ==========================================================
# 周期解析結果をクリア
# ----------------------------------------------------------
# 引数
#   qfx_decomposer: 周期解析器
# ==========================================================
def clear_analysis(qfx_decomposer: QfxDecomposer.QfxDecomposer):
    qfx_decomposer.clear_analysis()


# ==========================================================
# 周期解析
# ----------------------------------------------------------
# 引数
#   str_symbol:         銘柄名(symbol name)
#   str_time_frames:    時間足(identifier of bar's period)
#   n_samples:          サンプリング数(number of samples)
#   n_frequency:        頻度
# ----------------------------------------------------------
# 戻り地
#   処理が正常に終了した場合は True を返します。それ以外の場合は False を返します。
# ==========================================================
def analyze(
        str_symbol:         str,
        str_time_frames:    str,
        n_samples:          int,
        n_frequency:        int) -> bool:
    # ----------------------------------------------------------
    # 周期解析
    # ----------------------------------------------------------
    # Note
    #   周期解析器に指定された銘柄と時間足について、未解析のバーについて
    #   過去から順次解析します。
    # ----------------------------------------------------------
    qfx_mysql: QfxMySql.QfxMySql = QfxMySql.QfxMySql(_qfx_mysql_config)         # MySQL コネクタを生成
    if qfx_mysql.connect():                                                     # MySQL に接続・・・
        print("connected MySQL.")                                               # 通知
    else:                                                                       # 失敗したら・・・
        print("failed to connect MySQL.")                                       # エラー通知
        return False                                                            # 処理中断
    qfx_decomposer = create_decomposer(                                         # 周期解析器を生成
        qfx_mysql,                                                              # --- MySQL コネクタ
        str_symbol,                                                             # --- 銘柄名
        str_time_frames,                                                        # --- 時間足
        n_samples,                                                              # --- サンプリング数
        n_frequency)                                                            # --- 頻度
    b_ret: bool = True                                                          # 処理結果フラグを初期化
    try:                                                                        # 例外の捕捉を開始・・・
        n_analysis_times = qfx_decomposer.get_analysis_times()                  # 解析回数を取得
        for _ in tqdm(range(n_analysis_times)):                                 # ▽ループ開始
            n_input = QfxCommon.get_input_key_without_blocking()                # 入力キーを取得
            if n_input == ord("q"):                                             # [q] キーを入力したら・・・
                b_ret = False                                                   # 処理結果フラグを更新
                break                                                           # ループ中断
            if qfx_decomposer.analyze():                                        # 解析・・・
                qfx_decomposer.m_qfxMySql.commit()                              # コミット
            else:                                                               # 失敗したら・・・
                qfx_decomposer.m_qfxMySql.rollback()                            # ロールバック
                # qfx_decomposer.analyze() が以下の処理で False を返すケースがある。
                # dt_shift_left, dt_shift_right = self.get_sampling_range()		# 周期計算のサンプリング範囲を取得
        else:                                                                   # ループ中断をしなければ・・・
            print("completed.")                                                 # 通知
        if qfx_mysql.disconnect():                                              # MySQL を切断・・・
            print("disconnected MySQL.")                                        # エラー通知
        else:                                                                   # 失敗したら・・・
            print("failed to disconnect MySQL.")                                # エラー通知
    except KeyboardInterrupt:                                                   # Ctrl + C を押したとき・・・
        b_ret = False                                                           # 処理結果フラグを更新
        print("\nThis process will be suspended.")                              # 中断メッセージを通知
    return b_ret                                                                # 戻り地


# ==========================================================
# create a summary of price history
# ==========================================================
def create_summary_price_history():
    # ----------------------------------------------------------
    # MySQL データベースの価格履歴から銘柄と時間足の組を抽出します。
    # ここで抽出した銘柄と時間足の組について周期解析を行います。
    # ----------------------------------------------------------
    init_mysql_config()                                             # initialize configuration of MySQL
    global _df_summary_price_history                                # summary of number of bars by symbols and timeframes
    _df_summary_price_history = load_summary_price_history()        # total up the summary
    lst_table = QfxCommon.df_to_list(_df_summary_price_history)     # convert dataframe to list
    ascii_table = AsciiTable(lst_table)                             # construct a table
    print(ascii_table.table)                                        # show the table


# ==========================================================
# すべての銘柄と時間足の組を周期解析
# ==========================================================
def analyze_all():
    # ----------------------------------------------------------
    # MySQL データベースの価格履歴から銘柄と時間足の組を抽出します。
    # ここで抽出した銘柄と時間足の組について周期解析を行います。
    # ----------------------------------------------------------
    init_mysql_config()                                                         # Initialize configuration of MySQL
    df_count_total: pd.core.frame.DataFrame = load_summary_price_history()      # 銘柄と時間足ごとのデータ数の統計を取得
    lst_table = QfxCommon.df_to_list(df_count_total)                            # DataFrame をリストに変換
    ascii_table = AsciiTable(lst_table)                                         # 表を構成
    print(ascii_table.table)                                                    # 表を出力
    # ----------------------------------------------------------
    # 銘柄と時間足の組ごとに周期解析を実施
    # ----------------------------------------------------------
    for index, row in df_count_total.iterrows():                                # ▽ループ開始
        n_index: int = index                                                    # 対象の組のインデックスを取得
        str_symbol: str = row.symbol                                            # 銘柄名を取得
        str_time_frames: str = row.time_frames                                  # 時間足を取得
        print(                                                                  # 解析対象を通知
            "[%d] symbol=%s, time_frames=%s"                                    # --- 書式指定文字列
            % (n_index, str_symbol, str_time_frames))                           # --- パラメータ
        if not analyze(str_symbol, str_time_frames, _n_samples, _n_frequency):  # 周期解析・・・
            break                                                               # ループ中断
