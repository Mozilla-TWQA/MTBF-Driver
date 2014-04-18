#!/usr/bin/python
import re


## this is for getting MTBF_TIME translated to seconds
def time2sec(input_str):
    day = check_none_group(re.search('[^0-9]*([0-9]+)[Dd]', input_str))
    hour = check_none_group(re.search('[^0-9]*([0-9]+)[Hh]', input_str))
    minute = check_none_group(re.search('[^0-9]*([0-9]+)[Mm]', input_str))
    second = check_none_group(re.search('[^0-9]*([0-9]+)[Ss]', input_str))
    ret = ((day * 24 + hour) * 60 + minute) * 60 + second
    if(ret > 0):
        return ret
    raise ValueError


def check_none_group(m):
    if m is None:
        return 0
    return int(m.group(1))
