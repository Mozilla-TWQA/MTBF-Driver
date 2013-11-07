import os, time, sys, signal
from gaiatest import runtests
#import marionette.runtest.cli

class MTBF_Driver:
    def __init__(self, time):
        self.start_time = time;
        self.running_time = 0;


    ## logging module should be defined here

    def start_logging(self):
        pass

    def start_gaiatest(self):
        ## Infinite run before time expired

        try:
            while(True):
                ## Run test
                runtests.main()
                self.get_report()
        except Exception as e:
            ## Test run failed, halt?
            self.get_report()
            import traceback
            traceback.print_exc()
            raise Exception
            

    def get_report(self):
        pass

    def time_up(self, signum, frame):
        print 'Signal handler called with signal', signum
        raise IOError, "Time is up!"
        #sys.exit(0)


def main():
    mtbf = MTBF_Driver(os.getenv('MTBF_TIME', 120))  ## set default as 2 mins

    signal.signal(signal.SIGALRM, mtbf.time_up)
    signal.alarm(10)

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
