# coding=utf-8
# funnylab.org
# Date: 11-10-9
# Time: 上午2:18

__author__ = 'valorzhong'

def arr_to_str(arr):
    if isinstance(arr, list):
        s = ''
        for a in arr:
            if len(s) > 0:
                s += ', '
            if isinstance(a, list):
                s += '[' + arr_to_str(a) + ']'
            else:
                s += a
        return s
    else:
        return str(arr)