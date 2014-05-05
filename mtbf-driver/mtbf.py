import argparse
import logging
import os
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
    def __init__(self, time):
        self.duration = time
        self.start_time = None
        self.running_time = 0
        self.runner = None
        self.passed = 0
        self.failed = 0
        self.todo = 0
        self.level = 0
        mtbf_conf_file = os.getenv("MTBF_CONF", "conf/mtbf_config.json")
        with open(mtbf_conf_file) as json_file:
            self.conf = json.load(json_file)
        if self.conf['level']:
            self.level = self.conf['level']

    ## logging module should be defined here
    def start_logging(self):
        pass

    def start_gaiatest(self):
        step_log = 'last_replay.txt'
        rp = open(step_log, 'w')
        run_file = 'run_file.txt'  # TODO: default value, may not exist
        if self.conf['runlist'] and self.conf['runlist'].strip():
            run_file = self.conf['runlist']
        ## Infinite run before time expired
        runner_class = GaiaTestRunner
        parser_class = GaiaTestOptions
        parser = parser_class(
            usage='%prog [options] test_file_or_dir <test_file_or_dir> ...'
        )
        options, tests = parser.parse_args()
        parser.verify_usage(options, tests)
        self.start_time = time.time()
        sg = StepGen(level=self.level, root=self.conf['rootdir'], workspace=self.conf['workspace'], runlist=run_file)

        while(True):
            ## import only if config file states tools is there
            if self.conf['memory_report']:
                ## get some memory report before each round
                import tools.get_about_memory
                tools.get_about_memory.get_and_show_info(memory_report_args())

            ## Run test
            ## workaround: kill the runner and create another
            ## one each round, should be fixed
            self.runner = runner_class(**vars(options))
            tests = sg.generate()
            file_name, file_path = zip(*tests)
            rp.write(json.dumps(file_name) + "\n")
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
        os._exit(0)


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
    mtbf = MTBF_Driver(time)

    signal.signal(signal.SIGALRM, mtbf.time_up)
    signal.alarm(mtbf.duration)

    mtbf.start_gaiatest()
    signal.alarm(0)

if __name__ == '__main__':
    main()
