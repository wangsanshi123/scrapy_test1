#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import warnings
from collections import defaultdict

import baseutil
import timeutil
from builtinutil import div

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

class ParamObj(object):

    VALUE_FASAN = '$#$#ALL#$#$'

    def __init__(self, name, event_id, event_label, dict_params, func_start_date=None, func_end_date=None,
                 func_params=None, func_usenumber=None, func_duration=None, use_number=False,
                 result_has_duration=False, result_has_timedist=False, result_has_cntdist=True):
        self.event_id = event_id
        self.event_label = event_label
        self.dict_params = dict_params
        self.name = name
        self.func_start_date=func_start_date
        self.func_end_date=func_end_date
        self.func_params=func_params
        self.func_duration=func_duration
        self.func_usenumber=func_usenumber
        self.use_number=use_number
        self.result_has_duration = result_has_duration
        self.result_has_timedist = result_has_timedist
        self.result_has_cntdist = result_has_cntdist

    def __str__(self):
        return baseutil.join([self.event_id, self.event_label, str(self.dict_params), self.name], '____')

    def ok(self, event_id, event_label, params, start_date=None, end_date=None, usenumber=None, duration=None):
        is_start_date_ok = (not self.func_start_date) or self.func_start_date(start_date)
        is_end_date_ok = (duration is None) or (not self.func_end_date) or self.func_end_date(end_date)
        is_func_params_ok = (not self.func_params) or self.func_params(params)
        is_func_duration_ok = duration is None or not self.func_duration or self.func_duration(duration)
        is_func_usenumber_ok = usenumber is None or not self.func_usenumber or self.func_usenumber(usenumber)
        is_dictparams_ok = not {x[0]:x[1] for x in self.dict_params.items() if not (x[0] in params and x[1] == params[x[0]])}
        result = event_id == self.event_id and event_label == self.event_label \
               and is_dictparams_ok\
               and is_start_date_ok and is_end_date_ok and is_func_params_ok and is_func_duration_ok and is_func_usenumber_ok
        return result



class DataAnalysisEventsInfo(object):

    EVENTS_INFO_TYPE = 'EVENTS_INFO_TYPE'
    EVENTS_INFO_P_TYPE = 'EVENTS_INFO_P_TYPE'
    EVENTS_INFO_P_STICT_TYPE = 'EVENTS_INFO_P_STICT_TYPE'

    def __init__(self, datatype=EVENTS_INFO_TYPE):
        self.datatype = datatype
        self.dis = Distributor([1, 3, 6, 10, 20, 999999999])
        self.dis_duration = Distributor([3, 5, 10, 20, 999999999])
        self.funclist = list()

    def titles(self):
        return ['机型', '统计项', '样本量', '用户量', '用户率', '平均使用次数'] + '1次	2-3次	4-6次	7-13次	14-20次	21次及以上'.split('\t')

    def register_func(self, funca):
        '''
        stat方法运行时，会把每一条记录作为参数调用funca
        :param funca:
        :return:
        '''
        self.funclist.append(funca)

    def stat(self, dataset_iter, dict_modelyb, list_param, weekcount=1, duration_dist=False, time_dist=False, list_param_ext=None):
        '''
        :param dataset_iter:
        :param dict_modelyb:
        :param list_param:
        :param weekcount:
        :param duration_dist:是否返回时长分布
        :param time_dist:是否返回事件发生时间点分布
        :param list_param_ext:扩充的参数列表，这里面的ParamObj是特殊情况！
        :return:
        '''
        set_id_label = {baseutil.join([x.event_id, x.event_label], '____') for x in list_param}
        dict_model_param_imei_count = dict()
        dict_model_param_imei_duration = dict()
        dict_model_param_timedist = dict()

        for data in dataset_iter:
            if self.datatype == DataAnalysisEventsInfo.EVENTS_INFO_TYPE:
                imei, model, eventid, eventlabel, params, start_date, end_date, event_date, usenumber, duration = data[0], data[1], data[3], data[4], json.loads(data[14]), data[8], data[10], data[6], int(data[11]), int(data[12])
            elif self.datatype == DataAnalysisEventsInfo.EVENTS_INFO_P_TYPE:
                imei, model, eventid, eventlabel, params, start_date, end_date, event_date, usenumber, duration = data[0], data[1], data[14], data[15], json.loads(data[12]), data[6], data[8], data[4], int(data[9]), int(data[10])
            elif self.datatype == DataAnalysisEventsInfo.EVENTS_INFO_P_STICT_TYPE:
                model, simp_count, imei, eventid, eventlabel, params, start_date, end_date, event_date, usenumber, duration = \
                data[0], data[1], data[2], data[3], data[4], json.loads(data[5]), data[6], data[7], data[8], int(data[9]), int(data[10])
                dict_modelyb[model]=simp_count
            else:
                raise Exception('DataAnalysisEventsInfo.stat, 出现了异常的数据类型, datatype只能是{0}/{1}/{2}中的一种'.format(DataAnalysisEventsInfo.EVENTS_INFO_TYPE,
                                                                                                             DataAnalysisEventsInfo.EVENTS_INFO_P_TYPE,
                                                                                                             DataAnalysisEventsInfo.EVENTS_INFO_P_STICT_TYPE))
            for funca in self.funclist:
                funca(data)

            if not model in dict_modelyb:
                continue
            if not model in dict_model_param_imei_count:
                dict_model_param_imei_count[model] = dict()
                dict_model_param_imei_duration[model] = dict()
                dict_model_param_timedist[model] = dict()
            if baseutil.join([eventid, eventlabel], '____') not in set_id_label:
                continue
            try:
                list_param_ok = [x for x in list_param if x.ok(eventid, eventlabel, params, start_date, end_date, usenumber, duration)]
            except:
                print(list_param)
                print(eventid, eventlabel, params)
                raise
            for param_ok in list_param_ok:
                labelname = param_ok.name
                if not labelname in dict_model_param_imei_count[model]:
                    dict_model_param_imei_count[model][labelname] = defaultdict(int)
                    dict_model_param_imei_duration[model][labelname] = defaultdict(float)
                    dict_model_param_timedist[model][labelname] = [0 for _ in range(12)]
                dict_model_param_imei_count[model][labelname][imei] += usenumber if param_ok.use_number else 1
                dict_model_param_imei_duration[model][labelname][imei] += duration/60000
                dict_model_param_timedist[model][labelname][timeutil.time_hour2(timeutil.time_parse(event_date))] += usenumber if param_ok.use_number else 1
        dataset_out = list()
        for model, dict_param_imei_count in dict_model_param_imei_count.items():
            for param in list_param:
                if not param.name in dict_param_imei_count:
                    data = [model, param.name, dict_modelyb[model], 0, 0] + \
                        [0] + \
                        [0] * len(self.dis.get_threshold_names())
                    if duration_dist:
                        data += [0] + [0 for _ in self.dis_duration.get_threshold_names()]
                    if time_dist:
                        data += [0 for _ in range(12)]
                else:
                    dict_imei_count = {x[0]:div(x[1], weekcount) for x in dict_param_imei_count[param.name].items()}
                    dict_imei_duration = {x[0]: div(x[1], weekcount) for x in
                                          dict_model_param_imei_duration[model][param.name].items()}
                    usercount = len(dict_imei_count)
                    fenbu = self.dis.distribute(dict_imei_count)
                    data = [model, param.name, dict_modelyb[model], usercount, div(usercount, dict_modelyb[model])] + \
                        [div(sum(dict_imei_count.values()), usercount)]+ \
                        [div(x, usercount) for x in fenbu]
                    if duration_dist:
                        fenbu_duration = self.dis_duration.distribute(dict_imei_duration)
                        data += [div(sum(dict_model_param_imei_duration[model][param.name].values()), usercount)]
                        data += [div(x, usercount) for x in fenbu_duration]
                    if time_dist:
                        total = sum(dict_model_param_timedist[model][param.name])
                        data += [div(dict_model_param_timedist[model][param.name][x], total) for x in range(12)]
                dataset_out.append(data)
        return dataset_out


def group(dataset, list_func):
    '''
    分类，iter
    :param dataset:
    :param list_func:
    :return:
    '''
    def _gen_groupname(list_results):
        return '___'.join([x for x in list_results])
    for data in dataset:
        results = [x(data) for x in list_func]
        groupname = _gen_groupname(results)
        yield groupname, data



class Distributor(object):
    '''
    分布计算器
    '''
    def __init__(self, thresholds):
        '''
        :param thresholds: 第一个阈值应该是第一档的最大值，最后一个阈值应该是max，
        阈值作用是  (a, b]
        示例：[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        '''
        self._thresholds = thresholds

    def get_threshold_names(self):
        '''
        常规的阈值名称
        :return: 示例 ['<= 5', '5 - 10', '10 - 20', '> 20']
        '''
        names = list()
        for idx, x in enumerate(self._thresholds):
            if idx == 0:
                name = '<= %s' % x
            elif idx == len(self._thresholds)-1:
                name = '> %s' % self._thresholds[idx-1]
            else:
                name = '%s ~ %s' %(self._thresholds[idx-1], self._thresholds[idx])
            names.append(name)
        return names

    def __find_index(self, value):
        idx = 0
        for idx, thre in enumerate(self._thresholds):
            if value <= thre:
                break
        return idx

    def distribute(self, dict_a):
        arr_count = [0] * len(self._thresholds)
        for key, value in dict_a.items():
            arr_count[self.__find_index(value)] += 1
        return arr_count


DISTRIBUTOR_DURATION = Distributor([3, 5, 10, 20, 999999999])
DISTRIBUTOR_COUNT = Distributor([1, 3, 6, 10, 20, 999999999])

if __name__ == '__main__':
    dis = Distributor([5, 10, 20, 10000])
    print(dis.get_threshold_names())
    arrcount = dis.distribute({'a':20, 'b':30, 'c':10, 'd':2})
    print(arrcount)









