#!/usr/bin/python
import os
import os.path
import random
import json
import shutil
import logging

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


class StepGen(object):
    def __init__(self, workspace=None):
        self.setWorkspace(workspace)

    def setWorkspace(self, workspace):
        self.workspace = workspace
        if not os.path.exists(workspace):
            os.mkdir(workspace)

    def generate(self):
        raise NotImplementedError


class ReplayStepGen(StepGen):
    def __init__(self, workspace, replay):
        StepGen.__init__(self, workspace)
        self.setReplay(replay)

    def setReplay(self, replay_file):
        if not os.path.exists(replay_file):
            raise ValueError("Replay file " + replay_file + " does not exist.")
        self.replay = json.load(open(replay_file))["replay"]

    def generate(self):
        return map(lambda x: [x, x], self.replay)


class RandomStepGen(StepGen):
    def __init__(self, workspace=None, level=1, root=None, runlist=None, dummy=None):
        StepGen.__init__(self, workspace)
        self.max_level = 5
        if dummy is None:
            raise ValueError('fail to get dummy test case')
        self.dummy = (os.path.basename(dummy), dummy)
        self.setLevel(level)
        self.setRunlist(runlist)
        self.enqueue = []
        if(root):
            self.setRoot(root)
            self.loadFiles(root)

    def setLevel(self, level):
        '''
        level 0: No test but dummy
        level 1: One test and then dummy
        level 2: Two tests paired with one dummy
        level 3: Three tests
        level 4: Four tests
        level 5: No dummy cases
        '''
        if level >= 0 and level <= self.max_level:
            self.level = level

    def setRoot(self, root):
        self.root = root

    def setRunlist(self, runlist):
        with open(runlist) as fh:
            self.runlist = json.load(fh)['runlist']

    def loadFiles(self, root):
        to_run = set(self.runlist)
        uniq = set()
        for dir_path, dir_name, file_path in os.walk(root):
            for fp in file_path:
                full_path = os.path.join(dir_path, fp)
                if 'pyc' not in fp and fp in to_run and fp not in uniq:
                    uniq.add(fp)
                    shutil.copy2(full_path, self.workspace)
                    self.enqueue.append((fp, full_path))
        # logging not matched runlist items as warning
        logger.warning("Can't find following test cases: " + str(list(to_run - uniq)))
        if len(self.enqueue) == 0:
            raise ValueError("0 file in runlist is matched, root dir: ", root)

    def generate(self):
        '''
        from run list, randomly pick up test cases
        and return a list, write to file at the same time
        '''
        li = []
        for i in range(0, self.level):
            li.append(self.enqueue[random.randint(0, len(self.enqueue) - 1)])
        if self.level != self.max_level:
            pos = random.randint(0, self.level)
            li.insert(pos, self.dummy)
        return li


def main():
    run_file = 'tests/test_run.txt'
    sg = StepGen(level=3, root='/tmp/run_test', workspace='/tmp/replay', runlist=run_file)
    logger.debug('enqueue : ', sg.enqueue)
    import time
    while(True):
        time.sleep(1)
        logger.debug(sg.generate())

if __name__ == '__main__':
    main()
