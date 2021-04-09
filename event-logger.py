#!/usr/bin/env python

import subprocess as proc
import syslog
import sys
import time
while True:
    syslog.syslog(syslog.LOG_INFO | syslog.LOG_LOCAL4,'custom log - CAPACITY-1-UTILIZATION_HIGH')
    time.sleep(30)
