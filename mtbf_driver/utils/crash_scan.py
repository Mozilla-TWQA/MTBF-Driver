#!/usr/bin/python

import subprocess
import re

crash_stat_url = 'https://crash-stats.mozilla.com/report/index/'


def get_current_all_dev_serials():
    devices = []
    p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
    res = p.communicate()[0].split('\n')
    res.pop(0)
    for li in res:
        m = re.search('(\w+)', li)
        if(m is not None):
            devices.append(m.group(0))
    return devices


def get_crash_no_by_serial(serial):
    crash_num = 0
    cid = None
    base_dir = "/data/b2g/mozilla/Crash Reports/"
    scan_cmd = ['adb', '-s', serial, 'shell', 'ls -l']
    submit_dir = base_dir + 'submitted'
    pending_dir = base_dir + 'pending'
    p = subprocess.Popen(scan_cmd + [submit_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    pending_crash_file_list = set()
    if "No such" not in output:
        for out in output.split('\n'):
            if out.strip() != "":
                cid = re.search('\sbp-(\S+)\.txt$', out.strip()).group(1)
                crash_file_name = out.split(" ")[-1].split(".")[0]
                if crash_file_name not in pending_crash_file_list:
                    pending_crash_file_list.add(crash_file_name)
        crash_num += len(pending_crash_file_list)

    q = subprocess.Popen(scan_cmd + [pending_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = q.communicate()[0]
    pending_crash_file_list = set()
    if "No such" not in output:
        for out in output.split('\n'):
            if out.strip() != "":
                crash_file_name = out.split(" ")[-1].split(".")[0]
                if crash_file_name not in pending_crash_file_list:
                    pending_crash_file_list.add(crash_file_name)
        crash_num += len(pending_crash_file_list)

    return {"crashNo": crash_num, "cID": cid}


def main():
    serial_list = get_current_all_dev_serials()
    total_crash_num = 0
    for serial in serial_list:
        crash_data = get_crash_no_by_serial(serial)
        print("device " + serial + " has " + str(crash_data['crashNo']) + " crashes.")
        if crash_data['cID']:
            print("Submitted: " + crash_stat_url + crash_data['cID'])
        total_crash_num += crash_data['crashNo']
    print("Total crash number = " + str(total_crash_num))

if __name__ == "__main__":
    main()
