#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chilic'

import os
import fnmatch

DIR = "/home"
RELOAD = False


def getDirs():
    log_dirs = []
    dirs = os.listdir(DIR)
    for d in dirs:
        if os.path.isdir(os.path.join(DIR, d)):
            path = os.path.join(DIR, d, 'logs')
            if os.path.exists(path):
                log_dirs.append(path)
    return log_dirs


def getLogs(dirs):
    logs = []
    for logdir in dirs:
        for logfile in os.listdir(logdir):
            if fnmatch.fnmatch(logfile, '*.log'):
                logs.append(os.path.join(logdir, logfile))
    return logs

def rotate(logs, level=3):
    """

    :param logs:
    :param level:
    """
    for log in logs:
        if os.path.getsize(log) > 0:
            for i in range(1, level + 1):
                index = level - i

                if index == 0:
                    logfile = log
                    if os.path.exists(logfile):
                        newlogfile = '%s.%s' % (log, index + 1)
                        os.rename(logfile, newlogfile)
                        os.popen("gzip -f " + newlogfile)
                else:
                    logfile = '%s.%s.gz' % (log, index)
                    if os.path.exists(logfile):
                        newlogfile = '%s.%s.gz' % (log, index + 1)
                        os.rename(logfile, newlogfile)

                print "Rotate file: {0:s}".format(logfile)

if __name__ == '__main__':
    print "Start rotate"
    dirs = getDirs()
    logs = getLogs(dirs)
    rotate(logs)
    print "End rotate"
    print os.popen("/etc/init.d/apache2 reload").readlines()
