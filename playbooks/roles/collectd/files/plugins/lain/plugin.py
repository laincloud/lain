# -*- coding: utf-8 -*-


class Plugin(object):
    '''
    The base class for plugins
    All you need is just to extend it, overwrite prepare_data() method,
    and call report() method in __main__.
    '''

    def report(self):
        '''
        Report your prepared_data() to destination system
        '''
        data = self.prepare_data()
        self._report_to_graphite(data)

    def verbose(self):
        '''
        Show the data to the cluster administrators
        '''
        data = self.prepare_data()
        self._report_to_console(data)

    def prepare_data(self):
        '''
        Prepare your data. Return a list of DataItem(or its subclass) instances
        '''
        return []

    def _report_to_graphite(self, data):
        data_format = 'PUTVAL "%s/%s/%s" interval=%s N:%s'
        for item in data:
            data_map = item.format_data()
            print data_format % (data_map["endpoint"], data_map["metric"],
                                 data_map["type"], data_map["step"],
                                 data_map["value"])

    def _report_to_console(self, data):
        data_format = '%s %s %s'
        for item in data:
            data_map = item.format_data()
            val = data_map["value"]
            if data_map["type"] == "status":
                val = "OK" if data_map["value"] == 1 else "FAILED"
            print data_format % (data_map["endpoint"], data_map["metric"], val)


class DataItem(object):
    '''
    The base class of data items.
    If new monitor system is applied, we should support both new and old data
    format. So extend it and overwrite format_data() to satisfy new system, and
    modify old subclasses to make it capatible for old plugins
    '''

    def format_data(self):
        '''
        Formatting the data, return a dict
        '''
        return {}


class GraphiteData(DataItem):
    _metric = ""
    _endpoint = ""
    _value = ""
    _step = ""
    _type = ""

    def __init__(self, metric, endpoint,
                 value, step, type):
        self._metric = metric
        self._endpoint = endpoint
        self._value = value
        self._step = step
        self._type = type

    def format_data(self):
        return {
            "metric": self._metric,
            "endpoint": self._endpoint,
            "value": self._value,
            "step": self._step,
            "type": self._type,
        }
