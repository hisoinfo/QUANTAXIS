# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import time

import pandas as pd

from QUANTAXIS.QAFetch import QA_fetch_get_stock_transaction
from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_make_min_index


def QA_data_tick_resample(tick, type_='1min'):
    data = tick['price'].resample(
        type_, label='right', closed='left').ohlc()

    data['volume'] = tick['vol'].resample(
        type_, label='right', closed='left').sum()
    data['code'] = tick['code'][0]

    __data_ = pd.DataFrame()
    _temp = tick.drop_duplicates('date')['date']
    for item in _temp:
        __data = data[item]
        _data = __data[time(9, 31):time(11, 30)].append(
            __data[time(13, 1):time(15, 0)])
        __data_ = __data_.append(_data)

    __data_['datetime'] = __data_.index
    __data_['date'] = __data_['datetime'].apply(lambda x: str(x)[0:10])
    __data_['datetime'] = __data_['datetime'].apply(lambda x: str(x)[0:19])
    return __data_.fillna(method='ffill').set_index(['datetime', 'code'], drop=False)


if __name__ == '__main__':
    tick = QA_fetch_get_stock_transaction(
        'tdx', '000001', '2017-01-03', '2017-01-05')
    print(QA_data_tick_resample(tick))
