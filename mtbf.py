import os
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



def main():
    mtbf = MTBF_Driver(os.getenv('MTBF_TIME', 120))  ## set default as 2 mins
    mtbf.start_gaiatest()
    #TODO
    ## Create MTBF object isntance and run its main function

if __name__ == '__main__':
    main()
