#!/usr/bin/python
import subprocess
import re
import logging

logger = logging.getLogger(__name__)

class CrashReport(object):
    '''
    initial with test start time and monitor LastCrash
    if timestamp changed, increase crash number and update its time
    '''
    _crash_record = []
    crashed = False
    
    def __init__(self, start_time):
        self.start_time = start_time 
        subprocess.Popen(["adb", "shell", "rm", "/data/b2g/mozilla/Crash Reports/LastCrash"])

    def __len__(self):
        return len(self._crash_record)

    @property
    def lastCrash(self):
        if self._crash_record:
            return self._crash_record[-1]
        import time
        return time.time()

    def getCrashReport(self):
        '''
        Get latest crash time for LastCrash
        return new crash time list if updated
        '''
        cmd = subprocess.Popen(["adb", "shell", "cat", "/data/b2g/mozilla/Crash Reports/LastCrash"], stdout=subprocess.PIPE)
        ret = cmd.communicate()[0]
        crash_time = re.match("^[0-9]+$", ret)
        if crash_time is not None:
            crash_time = int(crash_time.group())
            if not self.crashed:
                self.crashed = True
            crash_record = set(self._crash_record)
            crash_record.add(crash_time)
            self._crash_record = sorted(list(crash_record))
            return self._crash_record
