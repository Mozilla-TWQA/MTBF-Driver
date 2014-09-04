import os
import sys
import os.path
import signal
import time
import json
import shutil
from gaiatest.runtests import GaiaTestRunner, GaiaTestOptions
from mozlog import structured

from utils.memory_report_args import memory_report_args
from utils.step_gen import RandomStepGen, ReplayStepGen
from utils.time_utils import time2sec


class MTBF_Driver:

    runner_class = GaiaTestRunner
    parser_class = GaiaTestOptions
    start_time = 0
    running_time = 0
    runner = None
    passed = 0
    failed = 0
    todo = 0
    level = 0
    ttr = []
    ori_dir = os.path.dirname(__file__)
    dummy = os.path.join(ori_dir, "tests", "test_dummy_case.py")

    ## time format here is seconds
    def __init__(self, time, rp=None):
        self.duration = time
        self.rp = rp
        self.load_config()

    def load_config(self):
        parser = self.parser_class(
            usage='%prog [options] test_file_or_dir <test_file_or_dir> ...'
        )
        structured.commandline.add_logging_group(parser)
        options, tests = parser.parse_args()
        parser.verify_usage(options, tests)
        self.options = options

        logger = structured.commandline.setup_logging(
        options.logger_name, options, {"tbpl": sys.stdout})

        options.logger = logger

        self.logger = logger

        conf = []
        mtbf_conf_file = os.getenv("MTBF_CONF", os.path.join(self.ori_dir, "conf/mtbf_config.json"))

        try:
            with open(mtbf_conf_file) as json_file:
                self.conf = json.load(json_file)
        except IOError:
            logger.error("IOError on ", mtbf_conf_file)
            sys.exit(1)

        ## assign folder for logs or debugging information in a folder
        if 'archive' in self.conf:
            self.archive_folder = os.path.join(os.getcwd(), self.conf['archive'])
        else:
            self.archive_folder = os.path.join(os.getcwd(), "output")

        if 'level' in self.conf:
            self.level = self.conf['level']
        if 'rootdir' not in self.conf or 'workspace' not in self.conf:
            logger.error('No rootdir or workspace set, please add in config')
            sys.exit(1)

        if 'runlist' in self.conf and self.conf['runlist'].strip():
            self.runlist = self.conf['runlist']
            if not os.path.exists(self.runlist):
                self.runlist = os.path.join(self.ori_dir, self.conf['runlist'])
                if not os.path.exists(self.runlist):
                    logger.error(self.conf['runlist'], " does not exist.")
                    sys.exit(1)

        self.rootdir = self.conf['rootdir']
        if not os.path.exists(self.rootdir):
            self.rootdir = os.path.join(self.ori_dir, self.conf['rootdir'])
            if not os.path.exists(self.rootdir):
                logger.error("Rootdir doesn't exist: " + self.conf['rootdir'])
                sys.exit(1)

        self.workspace = self.conf['workspace']
        if not os.path.exists(self.workspace):
            logger.info("Workspace doesn't exist, will create new one")
        return conf

    ## logging module should be defined here
    def start_logging(self):
        pass

    def start_gaiatest(self):
        ## Infinite run before time expired
        self.start_time = time.time()
        self.replay = os.getenv("MTBF_REPLAY")
        if self.replay:
            sg = ReplayStepGen(workspace=self.workspace, replay=self.replay)
        else:
            sg = RandomStepGen(level=self.level, root=self.rootdir, workspace=self.workspace, runlist=self.runlist, dummy=self.dummy)

        current_round = 0
        self.logger.info("Starting MTBF....")

        while(True):
            self.collect_metrics(current_round)
            current_round = current_round + 1

            ## Run test
            ## workaround: kill the runner and create another
            ## one each round, should be fixed

            self.runner = self.runner_class(**vars(self.options))
            tests = sg.generate()
            file_name, file_path = zip(*tests)
            self.ttr = self.ttr + list(file_name)
            self.runner.run_tests(file_path)
            self.passed = self.runner.passed + self.passed
            self.failed = self.runner.failed + self.failed
            self.todo = self.runner.todo + self.todo

            ## This is a temporary solution for stop the tests
            ## If there should be any interface there for us
            ## to detect continuous failure We can then
            ## remove this
            if self.runner.passed == 0:
                self.deinit()
                break

    def get_report(self):
        self.running_time = time.time() - self.start_time
        self.logger.info("\n*Total MTBF Time: %.3fs" % self.running_time)
        self.logger.info('\nMTBF TEST SUMMARY\n-----------------')
        self.logger.info('passed: %d' % self.passed)
        self.logger.info('failed: %d' % self.failed)
        self.logger.info('todo:   %d' % self.todo)

    def time_up(self, signum, frame):
        self.logger.info("Signal handler called with signal" + str(signum))
        self.deinit()
        os._exit(0)

    def deinit(self):
        virtual_home = os.getenv('VIRTUAL_ENV')
        self.get_report()
        serialized = dict()
        serialized['replay'] = self.ttr
        if self.rp:
            self.rp.write(json.dumps(serialized))
            self.rp.close()
            self.logger.info("Write reproduce steps finished")
            shutil.copy2(self.rp.name, os.path.join(self.workspace, "replay"))
        shutil.copy2(self.dummy, os.path.join(self.workspace, os.path.basename(self.dummy)))
        dest = os.path.join(self.workspace, os.path.basename(virtual_home))
        if not virtual_home == dest:
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(virtual_home, dest)
        info = os.path.join(virtual_home, 'info')
        if os.path.exists(info):
            shutil.copy2(info, self.workspace)

    def collect_metrics(self, current_round):
            current_working_folder = os.getcwd()
            ## create directory for logs or debugging information
            if not os.path.exists(self.archive_folder):
                os.makedirs(self.archive_folder)
            os.chdir(self.archive_folder)

            ## import only if config file states tools is there
            if 'memory_report' in self.conf and self.conf['memory_report']:
                ## get some memory report before each round
                import tools.get_about_memory
                tools.get_about_memory.get_and_show_info(memory_report_args())

            ## get logcat and dmesg
            if 'logcat' in self.conf and self.conf['logcat']:
                logcat_cmd = "adb logcat -v threadtime -d > logcat" + str(current_round)
                dmesg_cmd = "adb shell dmesg > dmesg" + str(current_round)
                os.system(logcat_cmd)
                os.system(dmesg_cmd)

            ## show us the overall status of the phone
            if 'overall_status' in self.conf and self.conf['overall_status']:
                bugreport_cmd = "adb shell dumpstate > bugreport" + str(current_round)
                os.system(bugreport_cmd)

            ## show us b2g status of the phone
            if 'b2g_status' in self.conf and self.conf['b2g_status']:
                b2ginfo_cmd = "adb shell b2g-info -t > b2ginfo" + str(current_round)
                b2gps_cmd = "adb shell b2g-ps -t -p -P --oom > b2gps" + str(current_round)
                b2gprocrank_cmd = "adb shell b2g-procrank --oom > b2gprocrank" + str(current_round)
                os.system(b2ginfo_cmd)
                os.system(b2gps_cmd)
                os.system(b2gprocrank_cmd)

            ## show us events
            if 'get_event' in self.conf and self.conf['get_event']:
                bugreport_cmd = "adb shell getevent -S > getevent" + str(current_round)
                os.system(bugreport_cmd)

            os.chdir(current_working_folder)


def main():
    ## set default as 2 mins
    try:
        time = int(time2sec(os.getenv('MTBF_TIME', '2m')))
    except ValueError:

        sys.stderr.write(
            "input value parse error: ",
            os.getenv('MTBF_TIME'),
            ", format should be '1d', '10h', '10m50s'\n"
        )
    step_log = 'last_replay.txt'
    rp = None
    if not os.getenv("MTBF_REPLAY"):
        rp = open(step_log, 'w')
    mtbf = MTBF_Driver(time, rp)
    if not os.getenv("MTBF_REPLAY"):
        signal.signal(signal.SIGALRM, mtbf.time_up)
        signal.alarm(mtbf.duration)
        try:
            mtbf.start_gaiatest()
        except Exception as e:
            mtbf.logger.error("Exception occurs: " + str(e))
            mtbf.deinit()
        signal.alarm(0)
    else:
        mtbf.start_gaiatest()


if __name__ == '__main__':
    main()
