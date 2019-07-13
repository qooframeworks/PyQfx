# coding: utf-8
import dataclasses
import datetime


# **********************************************************
# 価格シフト日時
# **********************************************************
@dataclasses.dataclass
class QfxPriceShiftTime:
    dtShiftLeft:    datetime.datetime = None
    dtShiftRight:   datetime.datetime = None
    dtShift:        datetime.datetime = None
