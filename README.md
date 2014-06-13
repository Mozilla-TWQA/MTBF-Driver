MTBF-Driver
===========

MTBF (Mean time between failures) is defined generally for mobile device stability testing (http://en.wikipedia.org/wiki/Mean_time_between_failures)

MTBF Driver is for performing long-term testing (over 100 hours) on Firefox OS devices automatically.
It uses marionette as test runner and gaia ui test as base library, emulate user's behavior randomly while no crash and hang is permitted.

# Environment
OSX or Linux-like operating system

# Installation
After cloning repository, please execute setup.py and install all dependancies.
Python virtual environment is recommended.

# Execution
You can find command sample in shell/mtbf.sh
MTBF_TIME=10h MTBF_CONF=conf/local.json mtbf --address=localhost:2828 --testvars=testvars.json tests/test_dummy_case.py

# Parameters
System variable:
```
MTBF_TIME
-- 

MTBF_CONF
```

Options in config file
```
{
  "memory_report": false,
  "logcat": true,
  "overall_status": true,
  "b2g_status": true,
  "get_event": true,
  "rootdir": "tests/mtbf",
  "workspace": "/tmp/workspace",
  "manifest_prefix": "mtbf",
  "archive": "output",
  "runlist": "runlist/all.list",
  "level": 4
}
```

memory report: Enable get_about_memory script during test run

logcat: Trigger logcat periodically

overall_status: Get android system info

b2g_status: Get b2g specific system info

get_event:

rootdir: Indicate search path of test case bank

workspace: A temporary directory to store running artifacts

manifest_prefix: Not used in production

archive: Not used in production

runlist: Specify test cases to be randomly executed

level: Robust magnitude, every round test runner will insert a dummy test case.  level equals to number of active test cases inserted.

       For example, 3 means in each round, 2 real test cases and 1 dummy test case scheduled.  Level 0 means no test cases executed but dummy.

       Level 5 is to disable dummy and run test in best effort.
