# Copyright 2020
#
# Created by nguyenvantam at 7/14/21
# Modified by nguyenvantam
#
# -*- coding: utf-8 -*-

import datetime

import isodate


def convert_ISO_8601_duration_to_seconds(duration):
    time_str = str(isodate.parse_duration(duration))
    date_time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
    return datetime.timedelta(hours=date_time_obj.hour, minutes=date_time_obj.minute,
                              seconds=date_time_obj.second).total_seconds()
