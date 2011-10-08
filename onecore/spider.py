# coding=utf-8
# funnylab.org
#
import logging
import os
import re
import urllib2
import time

__author__ = 'valorzhong'

def cleanup(origin):
    return remove_spaces(remove_tag(remove_style(remove_javascript(origin))))

def remove_tag(origin):
    return re.sub(r'<[^>]+>', '', origin)

def remove_javascript(origin):
    return re.sub(r'<script[\w\W]*?</script>', '', origin)

def remove_style(origin):
    return re.sub(r'<style[\w\W]*?</style>', '', origin)

def remove_spaces(origin):
    return re.sub(r'\s+', ' ', origin)

def remove_tag_attrs(origin):
    return re.sub(r'<([^>]*?)\s+.*?>', r'<\1>', origin)

def remove_non_chinese_characters(origin):
    return re.sub(r'^[\u300a\u300b]|[\u4e00-\u9fa5]|[\uFF00-\uFFEF]|\s+', '', origin)

def fetch(url, max_retry = 3, encoding='utf-8', error_sleep_second=1):
    result = None
    retry = 0
    while retry < max_retry:
        try:
            result = urllib2.urlopen(url).read().decode(encoding)
            retry = max_retry
        except Exception, err:
            retry += 1
            print str(err) + ', wait 1 seconds retry ' + str(retry) + ',' + url
            if retry < max_retry:
                time.sleep(error_sleep_second)
    return result

def download_file(url, save_to):
    """
    Please use downloader.py
    """
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = urllib2.Request(url)
    remote = opener.open(request)
    local = open(save_to, 'w')
    local.write(remote.read())
    local.close()
    remote.close()

def get_with_pattern(pattern, content, filter=None):
    match = re.search(pattern, content)
    if match:
        if filter:
            return filter(match.groups())
        return match.groups()
    return None

def list_with_pattern(pattern, content, filter=None):
    result = []
    iter = re.finditer(pattern, content)
    if iter:
        result = [m.groups() for m in iter]
    if filter:
        return filter(result)
    return result

def read_id(path, default=1):
    result = default
    try:
        reader = open(path, 'r')
        result = int(reader.readline())
        reader.close()
    except IOError:
        write_id(path, default)
    return result

def write_id(path, id):
    writer = open(path, 'w')
    writer.write(str(id))
    writer.flush()

def simple_launch(url_format, history_file, fetch_handler, fail_handler, default_start_id, max_invalid_count=20):
    start_id = read_id(history_file, default=default_start_id)
    invalid_count = 0
    max_invalid = max_invalid_count
    i = start_id
    while True:
        url = url_format % i
        content = fetch(url, max_retry=1)
        if content:
            invalid_count = 0
            fetch_handler(i, content)
            write_id(history_file, i)
        else:
            fail_handler(i)
            invalid_count += 1
            if invalid_count > max_invalid:
                break
        i += 1


if __name__ == '__main__':
    id = '59130'
    download_file('http://www.nduoa.com/apk/download/%s' % id, '/Users/searover/tmp/%s.apk' % id)