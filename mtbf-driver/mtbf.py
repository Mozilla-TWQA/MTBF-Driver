import argparse
import logging
import os
import sys
import os.path
import signal
import time
import json
from utils.time_utils import time2sec
from utils.step_gen import StepGen
from gaiatest.runtests import GaiaTestRunner, GaiaTestOptions


## this is for faking out an argument set for memory report
def memory_report_args(
        minimize=False,
        leave_on_device=False,
        no_auto_open=False,
        keep_report=False,
        gc_log=True,
        abbrev_gc_log=False):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--minimize',
        '-m',
        dest='minimize_memory_usage',
        action='store_true',
        default=minimize)
    parser.add_argument(
        '--directory',
        '-d',
        dest='output_directory',
        action='store',
        metavar='DIR')

    parser.add_argument(
        '--leave-on-device',
        '-l',
        dest='leave_on_device',
        action='store_true',
        default=leave_on_device)

    parser.add_argument(
        '--no-auto-open',
        '-o',
        dest='open_in_firefox',
        action='store_false',
        default=no_auto_open)
    parser.add_argument(
        '--keep-individual-reports',
        dest='keep_individual_reports',
        action='store_true',
        default=keep_report)

    gc_log_group = parser.add_mutually_exclusive_group()

    gc_log_group.add_argument(
        '--no-gc-cc-log',
        dest='get_gc_cc_logs',
        action='store_false',
        default=gc_log)

    gc_log_group.add_argument(
        '--abbreviated-gc-cc-log',
        dest='abbreviated_gc_cc_log',
        action='store_true',
        default=abbrev_gc_log)

    parser.add_argument('--no-dmd', action='store_true', default=False)

    args, unknown = parser.parse_known_args()
    return args


class MTBF_Driver:
    ## time format here is seconds
    def __init__(self, time, rp=None):
        self.duration = time
        self.start_time = None
        self.running_time = 0
        self.runner = None
        self.passed = 0
        self.failed = 0
        self.todo = 0
        self.level = 0
        self.rp = rp

    def load_config(self):
        conf = []
        mtbf_conf_file = os.getenv("MTBF_CONF", "conf/mtbf_config.json")
        try:
            with open(mtbf_conf_file) as json_file:
                self.conf = json.load(json_file)
        except IOError:
            print("IOError on ", mtbf_conf_file)
            sys.exit(1)
        if 'level' in self.conf:
            self.level = self.conf['level']
        if 'rootdir' not in self.conf or 'workspace' not in self.conf:
            print('No rootdir or workspace set, please add in config')
            sys.exit(1)
        run_file = 'run_file.txt'  # TODO: default value, may not exist
        if 'runlist' in self.conf and self.conf['runlist'].strip():
            self.runlist = self.conf['runlist']

        if not os.path.exists(self.conf['rootdir']):
            print("Rootdir doesn't exist")
            sys.exit(1)
        if not os.path.exists(self.conf['workspace']):
            print("Workspace doesn't exist")
            sys.exit(1)
        if not os.path.exists(run_file):
            print(run_file, " does not exist.")
            sys.exit(1)
        return conf

    ## logging module should be defined here
    def start_logging(self):
        pass

    def start_gaiatest(self):
        ## Infinite run before time expired
        runner_class = GaiaTestRunner
        parser_class = GaiaTestOptions
        parser = parser_class(
            usage='%prog [options] test_file_or_dir <test_file_or_dir> ...'
        )
        options, tests = parser.parse_args()
        parser.verify_usage(options, tests)
        self.start_time = time.time()
        sg = StepGen(level=self.level, root=self.conf['rootdir'], workspace=self.conf['workspace'], runlist=self.runlist)

        current_round = 0
        while(True):
            ## import only if config file states tools is there
            if 'memory_report' in self.conf and self.conf['memory_report']:
                ## get some memory report before each round
                import tools.get_about_memory
                tools.get_about_memory.get_and_show_info(memory_report_args())

            ## get logcat and dmesg
            if self.conf.has_key('logcat') and self.conf['logcat']:
                logcat_cmd = "adb logcat -v threadtime -d > logcat" + str(current_round)
                dmesg_cmd = "adb shell dmesg > dmesg" + str(current_round)
                os.system(logcat_cmd)
                os.system(dmesg_cmd)

            ## show us the overall status of the phone
            if self.conf.has_key('overall_status') and self.conf['overall_status']:
                bugreport_cmd = "adb shell dumpstate > bugreport" + str(current_round)
                os.system(bugreport_cmd)

            ## show us b2g status of the phone
            if self.conf.has_key('b2g_status') and self.conf['b2g_status']:
                b2ginfo_cmd = "adb shell b2g-info -t > b2ginfo" + str(current_round)
                b2gps_cmd = "adb shell b2g-ps -t -p -P --oom > b2gps" + str(current_round)
                b2gprocrank_cmd = "adb shell b2g-procrank --oom > b2gprocrank" + str(current_round)
                os.system(b2ginfo_cmd)
                os.system(b2gps_cmd)
                os.system(b2gprocrank_cmd)

            ## show us events
            if self.conf.has_key('get_event') and self.conf['get_event']:
                bugreport_cmd = "adb shell getevent -S > getevent" + str(current_round)
                os.system(bugreport_cmd)

            current_round = current_round + 1

            ## Run test
            ## workaround: kill the runner and create another
            ## one each round, should be fixed
            self.runner = runner_class(**vars(options))
            tests = sg.generate()
            file_name, file_path = zip(*tests)
            if self.rp:
                self.rp.write(json.dumps(file_name) + ",\n")
            self.runner.run_tests(file_path)
            self.passed = self.runner.passed + self.passed
            self.failed = self.runner.failed + self.failed
            self.todo = self.runner.todo + self.todo

            self.logger = logging.getLogger('Marionette')
            self.logger.handlers = []

            ## This is a temporary solution for stop the tests
            ## If there should be any interface there for us
            ## to detect continuous failure We can then
            ## remove this
            if self.runner.passed == 0:
                self.deinit()
                break

    def get_report(self):
        self.running_time = time.time() - self.start_time
        self.runner.logger.info("\n*Total MTBF Time: %.3fs", self.running_time)
        self.runner.logger.info('\nMTBF TEST SUMMARY\n-----------------')
        self.runner.logger.info('passed: %d' % self.passed)
        self.runner.logger.info('failed: %d' % self.failed)
        self.runner.logger.info('todo:   %d' % self.todo)

    def time_up(self, signum, frame):
        print(
            "Signal handler called with signal",
            signum
        )
        self.get_report()
        self.deinit()
        os._exit(0)

    def deinit(self):
        if self.rp:
            self.rp.write("]}")
            self.rp.close()


def main():
    ## set default as 2 mins
    try:
        time = int(time2sec(os.getenv('MTBF_TIME', '2m')))
    except ValueError:
        print(
            "input value parse error: ",
            os.getenv('MTBF_TIME'),
            ", format should be '1d', '10h', '10m50s'"
        )
    step_log = 'last_replay.txt'
    rp = open(step_log, 'w')
    rp.write("{ \"replay\": [\n")
    mtbf = MTBF_Driver(time, rp)

    signal.signal(signal.SIGALRM, mtbf.time_up)
    signal.alarm(mtbf.duration)

    mtbf.start_gaiatest()
    signal.alarm(0)

if __name__ == '__main__':
    main()
