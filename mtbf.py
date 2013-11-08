import os, time, sys, signal, logging
from gaiatest.runtests import GaiaTestRunner, GaiaTestOptions
from marionette.runtests import startTestRunner

class MTBF_Driver:
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
            self.runner = runner_class(**vars(options))
            self.runner.run_tests(tests)
            self.passed = self.runner.passed + self.passed
            self.failed = self.runner.failed + self.failed
            self.todo = self.runner.todo + self.todo
            
    def get_report(self):
        print("\nGenerate Report\n")
        self.running_time = time.time() - self.start_time
        self.runner.logger.info("\nTime taken %.3fs\n", self.running_time)
        
        
        self.runner.logger.info('\nSUMMARY\n-------')
        self.runner.logger.info('passed: %d' % self.passed)
        self.runner.logger.info('failed: %d' % self.failed)
        self.runner.logger.info('todo: %d' % self.todo)

    def time_up(self, signum, frame):
        print ("Signal handler called with signal", signum)
        self.get_report()
        raise KeyboardInterrupt
        #raise IOError, "Time is up!"
        #sys.exit(0)


def main():
    mtbf = MTBF_Driver(int(os.getenv('MTBF_TIME', 120))) ## set default as 2 mins

    signal.signal(signal.SIGALRM, mtbf.time_up)
    signal.alarm(mtbf.duration)

    mtbf.start_gaiatest()
    #TODO
    ## Create MTBF object isntance and run its main function
    
    # This open() may hang indefinitely
    #testalarm=1
    #while testalarm <=1:
    #    print "%s: %s" % ( 'mainprogram', time.ctime(time.time()) )
    #    time.sleep(1)


    signal.alarm(0)          # Disable the alarm

if __name__ == '__main__':
    main()
