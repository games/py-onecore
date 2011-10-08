# coding=utf-8
# funnylab.org
#
from httplib import HTTP
import os
from threading import Thread
import urllib
import time

__author__ = 'valorzhong'

class Task(object):
    url = ''
    save_to = ''
    tag = None
    will_redirect = False
    debug_level = 0
    block_number = 6
    complete_handler = None

class BlockThread(Thread):
    def __init__(self, task_name, url, filename, ranges):
        Thread.__init__(self, name=task_name)
        self.task_name = task_name
        self.url = url
        self.filename = filename
        self.ranges = ranges
        self.downloaded = 0
        # 16kb
        self.once_buffer = 16384

    def run(self):
        try:
            self.downloaded = os.path.getsize(self.filename)
        except OSError:
            self.downloaded = 0

        self.start_pointer = self.ranges[0] + self.downloaded
        if self.start_pointer >= self.ranges[1]:
            print '%s has been over.' % self.filename
            return

        types = urllib.splittype(self.url)
        host, res = urllib.splithost(types[1])
        h = HTTP()
        h.connect(host)
        h.putrequest('GET', res)
        h.putheader('Host', host)
        h.putheader('Range', "bytes=%d-%d" % (self.start_pointer, self.ranges[1]))
        h.endheaders()
        response = h._conn.getresponse()
        data = response.read(self.once_buffer)
        while data:
            file_opener = open(self.filename, 'ab+')
            file_opener.write(data)
            file_opener.close()
            self.downloaded += len(data)
            data = response.read(self.once_buffer)
        h.close()


def get_redirect_url(url):
    types = urllib.splittype(url)
    host, res = urllib.splithost(types[1])
    h = HTTP()
    h.connect(host)
    h.putrequest('HEAD', res)
    h.endheaders()
    status, reason, headers = h.getreply()
    return headers['location']

def get_file_size(url):
    types = urllib.splittype(url)
    host, res = urllib.splithost(types[1])
    h = HTTP()
    h.connect(host)
    h.putrequest('HEAD', res)
    h.putheader('Host', host)
    h.endheaders()
    status, reason, headers = h.getreply()
    return float(headers['Content-Length'])

def get_block_ranges(total_size, block_number):
    block_size = total_size / block_number
    ranges = []
    for i in range(0, block_number - 1):
        ranges.append((i * block_size, i * block_size + block_size - 1))
    ranges.append((block_size * (block_number - 1), total_size - 1))
    return ranges

def fetch(task):
    if os.path.exists(task.save_to):
        return

    if task.will_redirect:
        file_url = get_redirect_url(task.url)
    else:
        file_url = task.url
    file_size = get_file_size(file_url)
    ranges = get_block_ranges(file_size, task.block_number)

    task_names = ['task_%d' % i for i in range(0, task.block_number)]
    file_names = ['%s_%d.loading' % (task.save_to, i) for i in range(0, task.block_number)]

    treads = []
    for i in range(0, task.block_number):
        thread = BlockThread(task_names[i], file_url, file_names[i], ranges[i])
        thread.setDaemon(True)
        thread.start()
        treads.append(thread)

    def running():
        for thread in treads:
            if thread.isAlive():
                return  True
        return False

    time.sleep(1)
    while running():
        if task.debug_level > 0:
            total_downloaded = sum([thread.downloaded for thread in treads])
            process = total_downloaded / file_size * 100
            print '%db/%db - %d%s' % (total_downloaded, file_size, process, '%')
            if task.debug_level > 1:
                for thread in treads:
                    print '%s: %db - %s' % (thread.task_name, thread.downloaded, thread.filename)
        time.sleep(0.5)

    file_opener = open(task.save_to, 'wb+')
    for fn in file_names:
        f = open(fn, 'rb')
        file_opener.write(f.read())
        f.close()
        try:
            os.remove(fn)
        except OSError:
            pass
    file_opener.close()

    if task.complete_handler:
        task.complete_handler(task)

    if task.debug_level > 0:
        print 'Downloaded!!'


if __name__ == '__main__':

    id = '58813'

    def complete_handler(task):
        print 'finish!!'
    
    task = Task()
    task.url = 'http://www.nduoa.com/apk/download/%s' % id
    task.save_to = '/Users/searover/tmp/%s.apk' % id
    task.will_redirect = True
    task.debug_level = 2
    task.block_number = 6
    task.complete_handler = complete_handler

    fetch(task)












    





    