#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
import time
import calendar
# test
TIMEFORMAT_DEFAULT = '%Y-%m-%d %H:%M:%S'
TIMEFORMAT_ONLYDAY = '%Y-%m-%d'
TIMESPAN_DEFAULT = 2*60*60

def time_struct(time_insec):
    strct = time.localtime(time_insec)
    return strct

def now_insec():
    return time.time()

def now_instr():
    return time_format(time.time())

def date_today():
    '''
    今日日期
    :return:
    '''
    return time_format(time.time(), formatstr=TIMEFORMAT_ONLYDAY)

def time_format(time_inseconds, formatstr=TIMEFORMAT_DEFAULT):
    '''
    转换 seconds 值为格式化字符串
    Commonly used format codes:

    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.

    :param time_inseconds:
    :param formatstr:
    :return:
    '''
    return time.strftime(formatstr, time.localtime(time_inseconds))

def time_parse(time_instr, formatstr=TIMEFORMAT_DEFAULT):
    '''
    转换格式化字符串为 seconds 值
    Commonly used format codes:

    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.

    :param time_instr:
    :param formatstr:
    :return:
    '''
    return time.mktime(time.strptime(time_instr, formatstr))

def time_datebefore(time_now, days=1, formatstr=TIMEFORMAT_ONLYDAY):
    '''
    返回 前 days 天 的日期，字符串格式
    :param time_now: 可以是int型或日期类型
    :param days
    :param formatstr:
    :return:
    '''
    if type(time_now) == type(""):
        time_now = time_parse(time_now, TIMEFORMAT_ONLYDAY)
    time_lastday = time_now - 24*60*60 * days
    return time_format(time_lastday, formatstr)

def time_dayrelative(time_instr, formatstr=TIMEFORMAT_DEFAULT):
    '''
    计算 时间 相对于当天起始时间的 值，单位：s
    :param time_instr:
    :param formatstr:
    :return:
    '''
    cursecs = time_parse(time_instr, formatstr)
    daystartsecs = time_parse(time_format(cursecs, '%Y-%m-%d'), '%Y-%m-%d')
    sec_dayrelative = cursecs-daystartsecs
    return sec_dayrelative

def time_daystart(time_instr, formatstr=TIMEFORMAT_DEFAULT):
    '''
    计算当天起始时间，单位 s
    :param time_instr:
    :param formatstr:
    :return: seconds
    '''
    cursecs = time_parse(time_instr, formatstr)
    daystartsecs = time_parse(time_format(cursecs, '%Y-%m-%d'), '%Y-%m-%d')
    return daystartsecs


def time_hour2(time_sec):
    '''
    返回时间点所在时辰
    :param time_sec:
    :return:
    '''
    return time_struct(time_sec).tm_hour//2

arr_qujian = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24']
def time_qujian_span(timeindex):
    return arr_qujian[int(timeindex)]


def time_qujian(time_start, time_duration, timespan=TIMESPAN_DEFAULT, formatstr=TIMEFORMAT_DEFAULT):
    '''
    获取时间范围在各时间段内的时间长度
    :param time_start: 开始时间
    :param time_duration: 总时长， 单位：s
    :param timespan: 各时间区间的时间间隔
    :param formatstr: 开始时间的格式
    :return:
    '''
    def gen_realindex(indexa):
        return indexa%(int(24*60*60/timespan))
    time_start_daysec = time_dayrelative(time_start, formatstr)
    start_index = int(time_start_daysec/timespan)
    starttime_curspan = start_index * timespan
    dict_qujian = defaultdict(float)
    if time_start_daysec + time_duration < starttime_curspan + timespan:
        dict_qujian['%s'%gen_realindex(start_index)] += time_duration
    else:
        dict_qujian['%s'%start_index] += (start_index+1) * timespan - time_start_daysec
        time_duration -= (start_index+1) * timespan - time_start_daysec
        while time_duration > timespan:
            start_index += 1
            dict_qujian['%s'%gen_realindex(start_index)] += timespan
            time_duration -= timespan
        start_index += 1
        dict_qujian['%s'%gen_realindex(start_index)] += time_duration
    return dict_qujian

def gen_dates(date_from, date_end, day_gap):
    '''
    从 date_from - date_end ，以day_gap为间隔
    :param date_from:  字符串格式
    :param date_end:  字符串格式
    :param day_gap:  天数，int
    :return:
    '''
    time_from = time_parse(date_from, formatstr=TIMEFORMAT_ONLYDAY)
    time_end = time_parse(date_end, formatstr=TIMEFORMAT_ONLYDAY)
    time_gap = day_gap * 24 * 3600
    temp = time_from
    dates = list()
    while temp <= time_end:
        dates.append(temp)
        temp += time_gap

    dates = [time_format(x, formatstr=TIMEFORMAT_ONLYDAY) for x in dates]
    return dates

WEEK_DAYTYPE_WEEKDAY='工作日'
WEEK_DAYTYPE_WEEKEND='周末'

def week_daytype(date):
    '''
    返回工作日、周末
    WEEK_DAYTYPE_WEEKDAY / WEEK_DAYTYPE_WEEKEND
    :param date:
    :return:
    '''
    struct = time.localtime(time_parse(date, TIMEFORMAT_ONLYDAY))
    return WEEK_DAYTYPE_WEEKDAY if struct.tm_wday <= 4 else WEEK_DAYTYPE_WEEKEND

def week(time_str):
    return time.strftime('%W', time.localtime(time_parse(time_str)))

Monday = 'Monday'
Tuesday = 'Tuesday'
Wednesday = 'Wednesday'
Thursday = 'Thursday'
Friday = 'Friday'
Saturday = 'Saturday'
Sunday = 'Sunday'

WEEKDAYS = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]

def zhouji(time_str, formatstr=TIMEFORMAT_ONLYDAY):
    return time.strftime('%A', time.localtime(time_parse(time_str, formatstr)))

def zhouji_num(time_str, formatstr=TIMEFORMAT_ONLYDAY):
    '''
    一周内的第几天，从 周一/0 开始
    :param time_str:
    :param formatstr:
    :return:
    '''
    return WEEKDAYS.index(zhouji(time_str, formatstr))

def month_daycount(datea):
    '''
    计算某一月有多少天
    :param datea:
    :return:
    '''
    year, month, day = datea.split('-')
    year = int(year)
    month = int(month)
    firstweekday, daycount = calendar.monthrange(year, month)
    return daycount


def yueji_num(time_str, formatstr=TIMEFORMAT_ONLYDAY):
    '''
    一月内的第几天，从1号/0 开始
    :param time_str:
    :param formatstr:
    :return:
    '''
    return int(time_format(time_parse(time_str, formatstr), '%d'))-1

def get_week(weekidx):
    # 20160104
    strweek = time_format(
        time_parse('2016-01-04', TIMEFORMAT_ONLYDAY) + 24 * 3600 * 7 * weekidx,
        TIMEFORMAT_ONLYDAY)
    return strweek
# print(week('2016-01-03 01:01:01'))

ZERO = time_format(0, TIMEFORMAT_ONLYDAY)

# print(yueji_num('2017-03-01'))
# print(zhouji_num('2017-03-01'))


# print(week_daytype('2017-02-03'))

# print(zhouji('2017-03-05 09:01:01'))

# print(time_format(1481686856850/1000))

# print(gen_dates('2016-08-20', '2016-08-21', 1))

# print(time_format(0, formatstr=TIMEFORMAT_ONLYDAY))

#
# timea = time_format(1467072000, '%Y-%m-%d %H:%M:%S')
# print(timea)
# timeb = time_parse(timea, '%Y-%m-%d %H:%M:%S')
# print(timeb)
#
# dicta = time_qujian('2016-08-09 23:55:00', 60*60*4.5)
# print(dicta)

# print(time_format(572912407))

# print(time_struct(now_insec()))
# print(time_hour2(now_insec()))