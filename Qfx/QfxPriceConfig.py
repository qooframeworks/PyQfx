# coding=utf-8
import dataclasses


# **********************************************************
# QfxPriceConfig
# **********************************************************
@dataclasses.dataclass
class QfxPriceConfig:
    strSymbol:      str = "EURUSD"      # 銘柄名
    strTimeFrames:  str = "PERIOD_H1"   # 時間足
    nSamples:       int = 24 * 20       # サンプリング数
    nFrequency:     int = 24 * 5        # 頻度

