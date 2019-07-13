# coding=utf-8

# **********************************************************
# Import modules
# **********************************************************
import sys
import os
import datetime
import fcntl
import termios
import pandas as pd


# **********************************************************
# Common functions
# **********************************************************

# ==========================================================
# datetime.datetime 型を文字列に変換
# ----------------------------------------------------------
# 引数
#   dt: 日時
# ----------------------------------------------------------
# 戻り地
#   日時の文字列表現を返します。
# ==========================================================
def dt_to_str(dt: datetime.datetime) -> str:
    str_dt: str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return str_dt


# ==========================================================
# convert DataFrame to list
# ----------------------------------------------------------
# 引数
#   df: データフレーム
# ----------------------------------------------------------
# 戻り地
#   リストを返します。
# ==========================================================
def df_to_list(df: pd.core.frame.DataFrame) -> list:
    lst_table: list = df.reset_index().T.reset_index().T.values.tolist()
    return lst_table


# ==========================================================
# get input key without blocking process
# ----------------------------------------------------------
# Return:
#   key code inputted
# ==========================================================
def get_input_key_without_blocking() -> int:
    n_file_descripter: int = sys.stdin.fileno()                                     # 標準入力のファイルディスクリプタを取得
    lst_tc_attr_old: list[int] = termios.tcgetattr(n_file_descripter)               # 標準入力の端末属性を取得
    lst_tc_attr_new: list[int] = termios.tcgetattr(n_file_descripter)               # 標準入力の端末属性を取得
    lst_tc_attr_new[3] &= ~termios.ICANON                                           # lflags: カノニカルモードをオフ
    lst_tc_attr_new[3] &= ~termios.ECHO                                             # lflags: 入力文字を表示しない
    chr_input: int = 0                                                              # 入力文字格納バッファを初期化
    try:                                                                            # 例外の捕捉を開始
        termios.tcsetattr(n_file_descripter, termios.TCSADRAIN, lst_tc_attr_new)    # 標準入力の端末属性を更新
        n_fl_old: int = fcntl.fcntl(n_file_descripter, fcntl.F_GETFL)               # 標準入力の I/O 制御設定を取得
        fcntl.fcntl(n_file_descripter, fcntl.F_SETFL, n_fl_old | os.O_NONBLOCK)     # 入力待ちのブロッキングを行わない
        c = sys.stdin.read(1)                                                       # 入力文字を取得
        while len(c):                                                               # ▽ループ開始
            chr_input = (chr_input << 8) + ord(c)                                   # 文字を記録
            c = sys.stdin.read(1)                                                   # 入力文字を取得
    finally:                                                                        # 例外の捕捉を終了
        fcntl.fcntl(n_file_descripter, fcntl.F_SETFL, n_fl_old)                     # 標準入力の I/O 制御設定を元に戻す
        termios.tcsetattr(n_file_descripter, termios.TCSANOW, lst_tc_attr_old)      # 標準入力の端末属性を元に戻す
    return chr_input                                                                # 戻り地
