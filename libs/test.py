#!/usr/bin/python
# -*- coding: utf-8 -*-
from xlsxwriter import utility

import baseutil
import sqlite3
# from pyhive import hive

def test_dbfetch():
    src_db = r'E:\feedback_ui\data\db.db'
    conn = sqlite3.connect(src_db)
    cursor = conn.cursor()
    cursor.execute('select * from feedback_date')
    while True:
        data = cursor.fetchone()
        if not data:
            break
        print(data)

def find():
    list_paths = [r'C:\Users\Administrator\Desktop\2016-06-30.txt']
    results = baseutil.TxtFinder(list_paths).search('训练耗时')
    print('\n'.join([x[1] for x in results]))

def testhive():
    conn = hive.Connection(host="10.6.6.241", port=10000, username="syang")
    cursor = conn.cursor()
    cursor.execute("select * from datacollect.events_info where day='2016-07-01' limit 100")
    for result in cursor.fetchall():
        print(result)

'''
def add_chart_multiseries_line_new(sheet_name_chart, sheet_name_datasetsrc, series,
                                           title, start, width, height,
                                           xopt=None, yopt=None, y2opt=None, legendopt=None):
    worksheet = self._dict_sheet[sheet_name_chart]
    chart_num = self.add_chart({'type': 'line'})
    for name, value, seriesname in zip([names, values, seriesnames]):
        chart_num.add_series({'categories': "'%s'!%s" % (sheet_name_datasrc, name),
                              'values': '=%s!%s' % (sheet_name_datasrc, value),
                              'overlap': 10,
                              'name': seriesname})
    if xopt:
        chart_num.set_x_axis(xopt)
    if yopt:
        chart_num.set_y_axis(yopt)
    if y2opt:
        chart_num.set_y2_axis(y2opt)
    if legendopt:
        chart_num.set_legend(legendopt)
    chart_num.set_title({'name': title})
    chart_num.set_size({'width': width, 'height': height})
    worksheet.insert_chart(start, chart_num)
'''

def test_xlsxwriter():
    '''20170406 发起安装周报表格测试'''
    xlsxsrc = r'F:\工作\用户行为数据_SQL\分发市场应用数据\201702\test\分发市场统计_周报_2017-03-24.xlsx'
    reader = baseutil.XlsxReader(xlsxsrc)
    sn_install = '发起安装'
    dataset_active = reader.read_sheet(sn_install)

    xlsxout = r'F:\工作\用户行为数据_SQL\分发市场应用数据\201702\test\分发市场统计_测试.xlsx'
    wbout = baseutil.WorkBook(xlsxout)
    ws = wbout.add_sheet(sn_install, dataset_active)
    chart = wbout._workbook.add_chart({'type': 'line'})
    chart.set_y_axis({'name':'其他应用', 'magor_gridlines':{'line':{'color':'#B6C9F1'}}})
    chart.set_y2_axis({'name':'应用商店'})
    chart.set_chartarea({'fill':{'color':'#B6C9F1'}})

    chart.add_series({'categories': "'%s'!%s" % ('发起安装', utility.xl_range_abs(0, 2, 0, 34)),
                              'values': '=%s!%s' % ('发起安装', utility.xl_range_abs(1, 2, 1, 34)),
                              'overlap': 10,
                              'line':{'color':'blue'},
                              'y2_axis':True,
                              'name': '应用商店',
                                'marker':{'type':'square',
                                          'fill':{'color':'blue'},
                                          'border':{'color':'blue'}}})

    for x in range(2, 10):
        chart.add_series({'categories': "'%s'!%s" % ('发起安装', utility.xl_range_abs(0, 2, 0, 34)),
                       'values': '=%s!%s' % ('发起安装', utility.xl_range_abs(x, 2, x, 34)),
                       'overlap': 10,
                       'name': dataset_active[x][1],
                                'marker':{'type':'automatic'}})

    ws.insert_chart('A1', chart)

    wbout.close()





















if __name__ == '__main__':
    # find()
    # test_dbfetch()
    # testhive()
    test_xlsxwriter()