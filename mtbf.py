import os
import gaiatest.runtests
#import marionette.runtest.cli

class MTBF_Driver:
    def __init(self, time)__:
    self.start_time = time;
    self.running_time = 0;


    ## logging module should be defined here

    def start_logging():
        #TODO

    def start_gaiatest():
        ## Infinite run before time expired

        try:
            while(True):
                ## Run test
                runtests.main()
                get_report()



        except:
            ## Test run failed, halt?
            get_report()
            raise Exception
            

    def get_report():
        ## TODO



def main():
    mtbf = MTBF_Driver(os.getenv('MTBF_TIME', 120))  ## set default as 2 mins
    mtbf.start_gaiatest()
    #TODO
    ## Create MTBF object isntance and run its main function

if __name__ == '__main__':
    main()
