import logging
import os
import sys
import signal
import time

from gaiatest.runtests import GaiaTestRunner, GaiaTestOptions
from marionette.runtests import startTestRunner


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

    ## logging module should be defined here
    def start_logging(self):
        pass

    def start_gaiatest(self):
        ## Infinite run before time expired
        runner_class = GaiaTestRunner
        parser_class = GaiaTestOptions
        parser = parser_class(usage='%prog [options] test_file_or_dir <test_file_or_dir> ...')
        options, tests = parser.parse_args()
        parser.verify_usage(options, tests)
        self.start_time = time.time()

        while(True):
            ## Run test
            ## workaround: kill the runner and create another one each round, should be fixed
            self.runner = runner_class(**vars(options))
            self.runner.run_tests(tests)
            self.passed = self.runner.passed + self.passed
            self.failed = self.runner.failed + self.failed
            self.todo = self.runner.todo + self.todo

            self.logger = logging.getLogger('Marionette')
            self.logger.handlers = []

    def get_report(self):
        self.running_time = time.time() - self.start_time
        self.runner.logger.info("\n*Total MTBF Time: %.3fs", self.running_time)
        self.runner.logger.info('\nMTBF TEST SUMMARY\n-----------------')
        self.runner.logger.info('passed: %d' % self.passed)
        self.runner.logger.info('failed: %d' % self.failed)
        self.runner.logger.info('todo:   %d' % self.todo)

    def time_up(self, signum, frame):
        print ("Signal handler called with signal", signum)
        self.get_report()
        os._exit(0)


def main():
    ## set default as 2 mins
    time = int(os.getenv('MTBF_TIME', 2)) * 60
    mtbf = MTBF_Driver(time)

    signal.signal(signal.SIGALRM, mtbf.time_up)
    signal.alarm(mtbf.duration)

    mtbf.start_gaiatest()
    ## Disable the alarm
    signal.alarm(0)

if __name__ == '__main__':
    main()
